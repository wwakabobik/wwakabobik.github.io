#################################################
When Your ChromaDB Mutates and You’re Out of Luck
#################################################
:date: 2025-11-20 21:53
:author: wwakabobik
:tags: ai, python, chromadb, langchain, migration
:slug: migrating_chroma_db
:category: ai
:status: published
:summary: Migrating ChromaDB is painful, breaking, and full of edge cases. Here’s how we survived: dummy embeddings, JSON exports, private APIs, and a fully automated Python migration.
:cover: assets/images/bg/ai.png

Let’s set the stage.

Imagine: your AI agents have been running for months or years, diligently accumulating context, memories, embeddings, metadata — the whole in-silico biography of how they grew from simple scripts into semi-sentient companions that argue about breakfast choices.

And then ChromaDB drops a new major version.

Not just “minor API changes,” no. A *mutation.*
A biological one. The sort of mutation where your innocent goldfish suddenly grows limbs, starts quoting RFC standards, and demands a GPU.

New storage backend.
New API.
New import/export logic.
Old LangChain wrappers break spontaneously.
Python 3.13 refuses to compile DuckDB wheels like a unionized worker on strike.

Your AI wakes up without a memory. Congratulations — you’ve built a lobotomy machine.

Skipping migration was not an option. The stakes were obvious: without those embeddings, your agents become toddlers with broadband access — loud, confused, and unhelpful.

So this is the story of how we **refused to trust official tools**, hacked together a brutal but reliable pipeline, and force-migrated ChromaDB the way BOFH would migrate users off a shared NFS drive: quickly, painfully, mercilessly.

Why Migration Was Necessary
===========================

We originally ran ChromaDB `<0.7.0` wrapped with `langchain_chroma`. Back then, things were simple:

* Storage = SQLite
* Everything lived in a modest file
* API surface was stable enough to lull you into false confidence
* LangChain handled the wrapper logic without screaming

Then came ChromaDB 1.x. A rewrite. A reinvention. A complete flip of the table.

Breaking changes included:

* SQLite backend replaced with Parquet / DuckDB hybrid storage
* Entire internal API reorganized
* Several old methods removed (silently, of course)
* Embedding validation became strict
* LangChain wrappers changed shape
* The new Chroma auto-calls embedding APIs even when you give it precomputed vectors
* Token limits became a real-world hazard, not just a theoretical annoyance

Fun fact: in our database, single memory chunks could hit 3–4k tokens. Try recomputing that thousands of times through OpenAI’s embedding endpoint and watch your API key sob uncontrollably.

Here’s the punchline: migrating *in-place* was impossible. Nothing was compatible anymore — not the files, not the wrappers, not even the Python versions.

The Failures That Made Us Cry (and Swear)
=========================================

You’d think “use the official migration tool,” right?
Hahahah. No.

We tried all obvious paths. Each one was a unique flavor of pain.

1. `pip install chroma-migrate` → *kaboom*
--------------------------------------------

As soon as ChromaDB 1.x switched to DuckDB-based backend, everything older simply died.

`chroma-migrate` requires an ancient version of DuckDB.

Modern Python 3.13 cannot build that wheel.

.. code-block:: text

    error: command '/usr/bin/clang++' failed with exit code 1
    Failed building wheel for duckdb
    OSError: [Errno 9] Bad file descriptor

This was the moment I remembered all the times I mocked Java developers for Maven dependency hell.

2. Using old chroma-migrate CLI on modern env → *ImportError Armageddon*
------------------------------------------------------------------------

The old CLI assumed the existence of `chromadb.api.API`.
ChromaDB 1.x removed it entirely.

Running it led to:

.. code-block:: text

    ImportError: cannot import name 'API' from 'chromadb.api'

The best part? The library *installs fine*, but explodes the moment you try to use it. Schrödinger’s CLI.

3. Rebuilding DuckDB manually → *no*
------------------------------------

A delightful cocktail of:

* `brew install duckdb`
* custom `DUCKDB_HOME` vars
* C++ compilation flags that read like arcane runes
* mysterious linker errors
* and ChromaDB STILL refusing to load because it wants a specific wheel build with ABI pins

At some point I realized:
**Rebuilding DuckDB is a mini-devops project with a boss fight.**

Not doing that for a database migration.

The Painful Realization
-----------------------

The “official migration path” simply did not support:

* Python 3.13
* macOS ARM64
* modern ChromaDB
* modern LangChain
* modern embeddings logic

In short: we were on our own.

So we did the BOFH thing:
**Ignore the official tools, dump everything to JSON, and force-import it back.**

Our Brutal Solution (Because Gentle Solutions Don’t Work Here)
==============================================================

This architecture is based on the principle:

> "If the database refuses to speak your language, make it shut up and hand you JSON."

Step 0: Keep Calm and Dump JSON
-------------------------------

Instead of trying to coerce old ChromaDB into speaking to new ChromaDB, we extract everything into a universal, backend-agnostic intermediate format.

JSON.

The great equalizer. The diplomat among data formats.

We export:

* `documents`
* `embeddings`
* `metadatas`
* `ids`

All raw. All unmodified.

.. code-block:: python

    from langchain_chroma import Chroma
    import json

    collection = Chroma(collection_name="memory", persist_directory=old_path)
    data = collection.get(include=["documents", "embeddings", "metadatas"])

    export_data = {
        "memory": {
            "ids": [m["id"] for m in data["metadatas"]],
            "documents": data["documents"],
            "embeddings": [e.tolist() for e in data["embeddings"]],
            "metadatas": data["metadatas"]
        }
    }

    with open("chroma_export.json", "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

Why JSON?
---------

Because SQLite, Parquet, DuckDB — all of them change like teenagers discovering cyberpunk. JSON doesn't.

Step 1: Don’t Recompute Embeddings (Ever)
-----------------------------------------

LangChain’s new Chroma wrapper aggressively tries to call your embeddings backend whenever you insert documents.

This is… let’s call it “suboptimal” when:

* old embeddings dimension ≠ new model dimension
* token chunks are huge
* OpenAI charges money
* you don’t want to wait 40 minutes
* you’d like reproducibility instead of pray-and-retry

To prevent that, we override the embeddings provider with a **DummyEmbeddings** class that returns zero vectors but is never actually used for the real embeddings.

It’s the digital equivalent of handing the bouncer a cardboard cutout of yourself while you sneak into the club.

.. code-block:: python

    from langchain.embeddings.base import Embeddings

    class DummyEmbeddings(Embeddings):
        def embed_documents(self, texts):
            return [[0.0]] * len(texts)
        def embed_query(self, text):
            return [0.0]

Without this trick, everything falls apart.
LangChain tries to “rebuild your embeddings,” ChromaDB screams about mismatched shapes, OpenAI takes your money, and your migration collapses.

Step 2: Import Everything via Private API
-----------------------------------------

Public API? Haha. No.

`_collection.add(...)` still accepts precomputed embeddings, bulk inserts, and IDs. It’s “private,” yes, but we’ve already established that courtesy has left the building.

.. code-block:: python

    collection._collection.add(
        documents=data["documents"],
        metadatas=data["metadatas"],
        embeddings=data["embeddings"],
        ids=data["ids"]
    )

Reasons this works:

* bypasses LangChain validation madness
* bypasses OpenAI embedding calls
* bypasses the new “strict dimension” checks (because vectors match themselves)
* avoids huge performance penalties

Is it hacky?
Absolutely.
Is it reliable?
More than anything else we tried.

Step 3: Automate the Entire Pipeline
------------------------------------

Migration must be:

* reproducible
* auditable
* scriptable
* runnable on CI
* not relying on someone remembering that weird environment variable

So we created `migrate_chroma.py` which:

* installs old env
* exports JSON
* installs new env
* imports JSON

Full pipeline:

.. code-block:: python

    import subprocess
    import sys

    def run(cmd):
        print("[CMD]", " ".join(cmd))
        subprocess.check_call(cmd)

    run([sys.executable, "export_old_chroma.py", "--old-path", old_path, "--output", output_json])
    run([sys.executable, "import_new_chroma.py", "--new-path", new_path, "--input", output_json])

Brutal.
Deterministic.
Effective.

Why This Works and chroma-migrate Doesn’t
=========================================

1. No DuckDB wheel compilation
2. No legacy internal API usage
3. No OpenAI calls
4. No token overflows
5. No LangChain auto-embedding nonsense
6. Works on Python 3.13, macOS ARM, CI, Docker
7. Guaranteed ID + metadata consistency
8. JSON is easy to diff, verify, version, compress

Migrating via JSON gives you full control.
Everything else gives you full pain.

Additional Deep-Dive: Why ChromaDB Became So incompatible
=========================================================

A few architectural points for the curious:

* ChromaDB moved away from a pure key-value SQLite structure
* Instead it adopted a columnar, analytics-friendly storage model
* Parquet + DuckDB enables huge vector stores (millions of rows)
* But the migration from one to another is not isomorphic

SQLite stores:

* rows
* with arbitrary JSON blobs
* with minimal validation
* ideal for small agent memories

Parquet stores:

* typed columns
* strict schemas
* strong null/value constraints
* often incompatible with arbitrary, messy metadata

Thus the *real* root cause:
**ChromaDB 0.x and 1.x don’t share a common schema language.**

Therefore JSON intermediate format is the only sane choice.

Lessons Learned
===============

* Never trust official migration tools for fast-evolving libraries
* Private APIs are private only until you need them
* JSON is the Switzerland of data formats
* Precomputed embeddings are priceless — protect them
* Token limits are real, and they are coming for you
* If migration is painful, automate it
* If migration breaks, automate the breakage
* If all else fails, bring BOFH energy and write your own script

In the end, ChromaDB mutated.
LangChain mutated.
Python mutated.
Nothing worked.

But with a little JSON, a dummy embeddings class, and the willingness to use private APIs like a true sysadmin sociopath…

**our AI memories survived.**

And that’s all that matters.

Full code you can find in the `Repo`_. If you found this guide helpful, consider supporting my work via `BuyMeACoffee`_, `ThanksDev`_, or `DonationAlerts`_! Your support fuels more deep dives into the wild world of AI engineering. Thank you!

.. _Repo: https://github.com/wwakabobik/ai_engines/tree/master/utils/chromadb_migration
.. _BuyMeACoffee: https://www.buymeacoffee.com/wwakabobik
.. _ThanksDev: https://thanks.dev/wwakabobik
.. _DonationAlerts: https://www.donationalerts.com/r/rocketsciencegeek
