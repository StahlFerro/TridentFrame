<template>
  <div
    class="r-click-menu"
    ref="popper"
    v-show="isVisible"
    tabindex="-1"
    v-click-outside="close"
    @contextmenu.capture.prevent
    style="display: block;">
    <ul class="r-click-menu-options">
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
}

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
    open(evt, contextData) {
      console.log(this.referenceObject(evt));
      data.isVisible = true;
      data.contextData = contextData;
      
      if (this.popper) {
        this.popper.destroy();
      }

      this.popper = createPopper(this.referenceObject(evt), document.querySelector(".r-click-menu"), {
        placement: 'right-start',
        modifiers: {
          
        },
      });
      console.log(this.popper);
       // Recalculate position
      this.$nextTick(() => {
        // this.popper.scheduleUpdate();
      });
      
    },
    close() {
      data.isVisible = false;
      data.contextData = null;
      console.log("Closed Context Menu");
    },
    referenceObject(evt) {
      const left = evt.clientX;
      const top = evt.clientY;
      const right = left;
      const bottom = top;
      const clientWidth = 0;
      const clientHeight = 0;
      console.log(evt);
      console.log(left, top, right, bottom);
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
    if (this.popper !== undefined) {
      this.popper.destroy();
    }
  },
};

</script>
