Highlights:
   - **Intermediate representation**
      - Add inline docs to all statements (#2276) (by **xumingkuan**)
   - **Language and syntax**
      - Add ti.randn (#2266) (by **Andrew Sun**)

Full changelog:
   - [Lang] Add ti.randn (#2266) (by **Andrew Sun**)
   - [ir] [refactor] Rename StackXStmt to AdStackXStmt (#2283) (by **xumingkuan**)
   - [ir] Rename set_arg_nparray to set_arg_external_array (#2280) (by **xumingkuan**)
   - [ir] [refactor] Remove OffloadedStmt::step (#2282) (by **xumingkuan**)
   - [test] Add a test for range analysis of indices of reversed loops (#2279) (by **xumingkuan**)
   - [refactor] Remove legacy C++ frontend macros (#2278) (by **Robslhc**)
   - [IR] Add inline docs to all statements (#2276) (by **xumingkuan**)
   - [ir] Rename is_np_array to is_external_array except the frontend (#2277) (by **xumingkuan**)
   - [opt] Avoid recursively generating indices twice for BLS (#2272) (by **xumingkuan**)
   - [refactor] Unified ti_core usage to _ti_core in python/taichi/misc, python/taichi/main and testing. (#2270) (by **Jiasheng Zhang**)
   - [misc] Update README.md (#2269) (by **Yuanming Hu**)
   - [ir] Move uniquely_accessed_bit_structs from compile_to_offloads to AnalysisManager (#2264) (by **xumingkuan**)
   - [ir] Remove type_check in clone (#2262) (by **xumingkuan**)
   - [type] [opt] Use BitStructStoreStmt for CustomFloatType with non-shared exponents (#2259) (by **xumingkuan**)
