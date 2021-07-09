<template>
  <mark>
    <Token v-bind:token="token" />
    <span class="tag" :style="{backgroundColor: classColorMap[token.label]}">
      {{ token.label }}
    </span>
  </mark>
</template>
<script>
import Token from "./Token";

export default {
  name: "EntityBlock",
  emits: ["remove-block"],
  data:function() {
    return {
      showClose: false,
    }
  },
  props: {
    token: {
      type: Object,
      requried: true
    },
    classColorMap: {
      type: Object,
      required: true
    },
  },
  components: {
    Token
  }
}
</script>

<style lang="scss">
mark {
  padding: 0.5rem;
  position: relative;
  background-color: burlywood;
  &::after {
    content: var(--tag);
    padding: 0.3rem;
    color: darkslategray;
    font-size: small;
  }
}
.close-btn {
  cursor: pointer;
  font-size: small;
  position: absolute;
  width: 1rem;
  height:1rem;
  padding-left: 0.2rem;
  border-radius: 50%;
  background-color: black;
  color: white;
}
.delete {
  margin-left: 10px;
}
</style>