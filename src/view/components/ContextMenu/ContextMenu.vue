<template>
  <div
    v-show="isVisible" :id="ctxMenuId" ref="popper" v-click-outside="emitOutsideClick" class="context-menu"
    tabindex="-1" style="display: block;" @contextmenu.capture.prevent
  >
    <ul class="context-menu-options">
      <!-- <li v-for="(ctxItemData, ctxItemIndex) in contextData" :key="ctxItemIndex" 
          @click="callOptionFunction(ctxItemData.callback);"
      > -->
      <li v-for="(ctxItemData, ctxItemIndex) in contextData" :key="ctxItemIndex" 
          @click="$emit('ctx-option-click', $event, ctxItemData.id)"
      >
        <slot name="contextMenuItem" v-bind="ctxItemData" />
      </li>
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

export default {
  directives: {
    // ClickOutside,
    clickOutside: vClickOutside.directive
  },
  props: {
    ctxMenuId: {
      type: String,
      required: true,
    },
    boundariesElement: {
      type: String,
      default: "body",
    },
    anchorElementId: {
      type: String,
      default: "",
      required: false,
    },
    placement: {
      type: String,
      default: "right-start",
      required: false,
    }
  },
  emits: ['ctx-menu-click-outside', 'ctx-option-click'],
  // components: {
  //   popper,
  // },
  data() {
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
    openPopper(event, contextData) {
      console.log(event);
      console.log(contextData);
      this.isVisible = true;
      this.contextData = contextData;
      this.originalEvent = event;
      if (this.rcmPopper) {
        this.rcmPopper.destroy();
      }

      const anchorPointElement = this.anchorElementId? document.querySelector(`#${this.anchorElementId}`) : this.referenceObject(event);
      const contextMenuElement = document.querySelector(`#${this.ctxMenuId}`)

      this.rcmPopper = createPopper(anchorPointElement, contextMenuElement, {
          placement: this.placement,
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
    emitOutsideClick(event) {
      this.$emit('ctx-menu-click-outside', event, this.ctxMenuId);
    },  
    closePopper(event) {
      console.log(`Closed Context Menu`);
      this.isVisible = false;
      this.contextData = null;
      this.originalEvent = null;
      console.log(this.$parent);
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
