<template>
  <div
    id="generalRClickMenu"
    class="context-menu"
    ref="popper"
    v-show="isVisible"
    tabindex="-1"
    v-click-outside="closePopper"
    @contextmenu.capture.prevent
    style="display: block;">
    <ul class="context-menu-options">
      <slot :contextData="contextData" />
    </ul>
  </div>
</template>

<script>
import { popper, createPopper } from '@popperjs/core';
import ClickOutside from 'vue-click-outside';
console.log(`POPPER`);
console.log(`CLICKOUTSIDE`);
console.log(ClickOutside)
// @vue/component
let data = {
  isVisible: false,
  contextData: {},
  originalEvent: null,
  rcmPopper: null,
}

function openPopper(evt, contextData) {
  data.isVisible = true;
  data.contextData = contextData;
  data.originalEvent = evt;
  if (data.rcmPopper) {
    data.rcmPopper.destroy();
  }

  data.rcmPopper = createPopper(this.referenceObject(evt), document.querySelector("#generalRClickMenu"), {
    placement: 'right-start',
    modifiers: {
    },
  });
    // Recalculate position
  this.$nextTick(() => {
    // this.popper.scheduleUpdate();
  });
}

function callOptionFunction(callback) {
  callback(data.originalEvent);
  closePopper();
}

function closePopper() {
  data.isVisible = false;
  data.contextData = null;
  data.originalEvent = null;
  console.log("Closed Context Menu");
}

window.onresize = closePopper;

export default {
  props: {
    boundariesElement: {
      type: String,
      default: 'body',
    },
  },
  // components: {
  //   popper,
  // },
  data: function () {
    return data;
  },
  directives:{
    ClickOutside,
  },
  methods: {
    openPopper: openPopper,
    callOptionFunction: callOptionFunction,
    closePopper: closePopper,
    referenceObject(evt) {
      const left = evt.clientX;
      const top = evt.clientY;
      const right = left;
      const bottom = top;
      const clientWidth = 0;
      const clientHeight = 0;
      return {
        getBoundingClientRect: () => ({
          width: 0,
          height: 0,
          top: top,
          right: left,
          left: left,
          bottom: top,
        })
      };
    },
  },
  beforeDestroy() {
    if (data.rcmPopper !== undefined) {
      data.rcmPopper.destroy();
    }
  },
};

</script>
