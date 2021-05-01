# Contributing to Concordium

The following is a list of core repositories of the Concordium organization, listing relationship between them, and guidelines for contribution.

## General structure

The components of the concordium node and related tools are distributed among a number of repositories. The majority of components are written in either Rust, Haskell, or a combination of the two, with some scripts and tools in a combination of Bash, Python, Typescript and Elm.

Dependencies are managed in two ways. If a packages is published in a tool-specific package registry, i.e., [crates.io](https://crates.io) for Rust and [stackage](https://www.stackage.org) then the dependency is taken from there, via the Cargo tool for Rust, and stack tool for Haskell.

If a dependency is not published in a package registry then we add it a git submodule dependency and refer to it as a local dependency. This latter method is also used if we need a fork of an existing package to either fix issues, or expose additional functionality not directly exposed by a published package.

As a general rule, if a repository A is a submodule dependency of repository B then if a change is made in A it should be propagated to B with a corresponding pull request. This is not a hard rule, but only a guideline, because repositories contain libraries as well as tools, so if a change does not affect upstream code then it is not necessary to immediately propagate it.

## Repositories

- [concordium-node](https://github.com/Concordium/concordium-node):
  This is the main node repository that contains, among other things
  - implementation of the full node running Concordium's protocols (consensus, finalization, network layer, state components)
  - bootstrapper node

  The repository has the following submodule dependencies on other Concordium repositories
  - [concordium-base](https://github.com/Concordium/concordium-base)
  - [concordium-grpc-api](https://github.com/Concordium/concordium-grpc-api)
  - [concordium-wasm-smart-contracts](https://github.com/Concordium/concordium-wasm-smart-contracts)
  - [haskell-lmdb](https://github.com/Concordium/haskell-lmdb/)

- [concordium-base](https://github.com/Concordium/concordium-base):
  This contains common libraries used by the node and other components. It defines common types, APIs and tools. It also contains the implementation of all cryptographic protocols used by the Concordium blockchain.

  This repository does not have any submodule dependencies.

- [concordium-grpc-api](https://github.com/Concordium/concordium-grpc-api):
  Contains the definition of the GRPC/Protobuf API that the node exposes. 

  This repository does not have any submodule dependencies.

- [concordium-**wasm**-smart-contracts](https://github.com/Concordium/concordium-wasm-smart-contracts):
  Contains the implementation of the on-chain functionality for smart contracts on the Concordium blockchain. This consists of a [Wasm](https://webassembly.org/) validator, interpreter, and integration with the node. Additionally, this repository contains the tool `cargo-concordium` for testing smart contracts.

  This repository has no submodule dependencies, but some of the packages in it do depend on [concordium-contracts-common](https://docs.rs/concordium-contracts-common/) Rust crate which is published on [crates.io](https://crates.io)

- [concordium-**rust**-smart-contracts](https://github.com/Concordium/concordium-rust-smart-contracts):
  Is the dual of [concordium-**wasm**-smart-contracts](https://github.com/Concordium/concordium-wasm-smart-contracts) that contains the Rust SDK for writing smart contracts for the Concordium blockchain. The main package in the repository is [concordium-std](https://docs.rs/concordium-std) which provides a form of a "standard library" for writing smart contracts.

  This repository has no submodule dependencies, but some of the packages in it do depend on [concordium-contracts-common](https://docs.rs/concordium-contracts-common/) Rust crate which is published on [crates.io](https://crates.io)

- [concordium-contracts-common](https://github.com/Concordium/concordium-contracts-common): Contains the implementation of some common functionality needed by both packages in [concordium-**rust**-smart-contracts](https://github.com/Concordium/concordium-rust-smart-contracts) and packages in [concordium-**wasm**-smart-contracts](https://github.com/Concordium/concordium-wasm-smart-contracts).

- [haskell-lmdb](https://github.com/Concordium/haskell-lmdb/): is a fork of [dmbarbour/haskell-lmdb](https://github.com/dmbarbour/haskell-lmdb) containing a number of bugfixes and exposing additional functionality.

- [concordium-client](https://github.com/Concordium/concordium-client): Is the main client that can be used to interact with a running node, including querying the state of the blockchain, sending transactions, updating smart contracts.

  This repository has the following submodule dependencies.
  - [concordium-base](https://github.com/Concordium/concordium-base)
  - [concordium-grpc-api](https://github.com/Concordium/concordium-grpc-api)

- [concordium-wallet-proxy](https://github.com/Concordium/concordium-wallet-proxy): This is a proxy server that exposes an API that is easier and safer to use by the mobile wallet than the node's GRPC interface.
  This repository has the following submodule dependencies (directly or transitively)
  - [concordium-client](https://github.com/Concordium/concordium-client) (direct dependency)
  - [concordium-base](https://github.com/Concordium/concordium-base) (via concordium-client)
  - [concordium-grpc-api](https://github.com/Concordium/concordium-grpc-api) (via concordium-client)

- [concordium-node-dashboard](https://github.com/Concordium/concordium-node-dashboard)
  This repository contains the implementation of a "node dashboard" which displays the status of a single node. It needs access to the node's API.

  This repository has the following submodule dependency.
  - [concordium-grpc-api](https://github.com/Concordium/concordium-grpc-api)

- [concordium-network-dashboard](https://github.com/Concordium/concordium-network-dashboard)
  This repository contains the implementation of the network dashboard which displays the status of the nodes which choose to report it.

## CI

We use github actions for continuous testing. As a general rule actions are run on every pull request against the `main` branch, and on every push to the `main` branch.

## Default branch

All repositories should use `main` as the default branch, as is default on github.

## Issues


## [.github](https://github.com/Concordium/.github)
   The common templates for contributions, pull requests, and issues are stored in [.github](https://github.com/Concordium/.github).
   If a new repository is added, an existing one removed or renamed, then this should be reflected in the contribution guidelines.

## Contributor license agreement

**This applies to external contributors only**, i.e., those **not** part of the Concordium group.

If you are such a person then as part of a pull request contributing changes you must acknowledge acceptance of the Contributors License Agreement.
