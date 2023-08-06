<!-- Copyright 2021 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div class="card bg-light">
    <div class="mt-3 mx-3">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <button type="button" class="btn btn-sm btn-light text-muted" @click="showMarkdown = !showMarkdown">
          <i class="fas fa-code" v-if="showMarkdown"></i>
          <i class="fas fa-eye" v-else></i>
        </button>
        <small class="text-muted" v-if="encoding">
          {{ i18n.t('misc.detectedEncoding') }} {{ encoding.toUpperCase() }}
        </small>
      </div>
      <markdown-preview :input="text" v-show="showMarkdown"></markdown-preview>
      <text-viewer :text="text" :show-border="false" v-show="!showMarkdown"></text-viewer>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showMarkdown: true,
    };
  },
  props: {
    text: String,
    encoding: {
      type: String,
      default: null,
    },
  },
};
</script>
