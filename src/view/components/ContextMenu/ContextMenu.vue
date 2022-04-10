<template>
  <div
    v-show="isVisible" id="generalRClickMenu" ref="popper" v-click-outside="closePopper" class="context-menu"
    tabindex="-1" style="display: block;" @contextmenu.capture.prevent
  >
    <ul class="context-menu-options">
      <slot :contextData="contextData" />
    </ul>
  </div>
</template>

<script>
import { popper, createPopper } from "@popperjs/core";
// import ClickOutside from "vue-click-outside";
import vClickOutside from 'click-outside-vue3'
console.log(`POPPER`);
console.log(`CLICKOUTSIDE`);
console.log(vClickOutside);
// @vue/component


// function openPopper(evt, contextData) {
//   data.isVisible = true;
//   data.contextData = contextData;
//   data.originalEvent = evt;
//   if (data.rcmPopper) {
//     data.rcmPopper.destroy();
//   }

//   data.rcmPopper = createPopper(
//     this.referenceObject(evt),
//     document.querySelector("#generalRClickMenu"),
//     {
//       placement: "right-start",
//       modifiers: {},
//     }
//   );
//   // Recalculate position
//   this.$nextTick(() => {
//     // this.popper.scheduleUpdate();
//   });
// }

// function callOptionFunction(callback) {
//   callback(data.originalEvent);
//   closePopper();
// }

// function closePopper() {
//   data.isVisible = false;
//   data.contextData = null;
//   data.originalEvent = null;
//   console.log("Closed Context Menu");
// }

// window.onresize = closePopper;

export default {
  directives: {
    // ClickOutside,
    clickOutside: vClickOutside.directive
  },
  props: {
    boundariesElement: {
      type: String,
      default: "body",
    },
  },
  // components: {
  //   popper,
  // },
  data: function() {
    return {
      isVisible: false,
      contextData: {},
      originalEvent: null,
      rcmPopper: null,
    };
  },
  beforeUnmount() {
    if (this.rcmPopper !== undefined) {
      this.rcmPopper.destroy();
    }
  },
  methods: {
    openPopper(evt, contextData) {
      this.isVisible = true;
      this.contextData = contextData;
      this.originalEvent = evt;
      if (this.rcmPopper) {
        this.rcmPopper.destroy();
      }

      this.rcmPopper = createPopper(
        this.referenceObject(evt),
        document.querySelector("#generalRClickMenu"), {
          placement: "right-start",
        }
      );
      // Recalculate position
      this.$nextTick(() => {
        // this.popper.scheduleUpdate();
      });
    },
    callOptionFunction(callback) {
      callback(this.originalEvent);
      this.closePopper();
    },
    closePopper() {
      this.isVisible = false;
      this.contextData = null;
      this.originalEvent = null;
      console.log("Closed Context Menu");
    },
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
        }),
      };
    },
  },
};
</script>
