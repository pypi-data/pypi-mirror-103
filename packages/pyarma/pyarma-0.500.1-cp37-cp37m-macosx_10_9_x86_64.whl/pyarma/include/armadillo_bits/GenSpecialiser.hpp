// Copyright 2008-2016 Conrad Sanderson (http://conradsanderson.id.au)
// Copyright 2008-2016 National ICT Australia (NICTA)
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ------------------------------------------------------------------------


//! \addtogroup GenSpecialiser
//! @{


template<typename elem_type, bool is_gen_zeros, bool is_gen_ones, bool is_gen_randu, bool is_gen_randn>
struct GenSpecialiser
  {
  arma_inline elem_type generate() const { return elem_type(); }
  };


template<typename elem_type>
struct GenSpecialiser<elem_type, true, false, false, false>
  {
  arma_inline elem_type generate() const { return elem_type(0); }
  };


template<typename elem_type>
struct GenSpecialiser<elem_type, false, true, false, false>
  {
  arma_inline elem_type generate() const { return elem_type(1); }
  };


template<typename elem_type>
struct GenSpecialiser<elem_type, false, false, true, false>
  {
  arma_inline elem_type generate() const { return elem_type(arma_rng::randu<elem_type>()); }
  };


template<typename elem_type>
struct GenSpecialiser<elem_type, false, false, false, true>
  {
  arma_inline elem_type generate() const { return elem_type(arma_rng::randn<elem_type>()); }
  };


//! @}
