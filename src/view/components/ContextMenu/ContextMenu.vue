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
  emits: ['ctx-menu-open', 'ctx-option-click', 'ctx-menu-click-outside',],
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
      this.$emit('ctx-menu-open', event);
    },
    callOptionFunction(callback) {
      callback(this.originalEvent);
      this.closePopper();
    },
    emitOutsideClick(event) {
      console.debug(`=== emitOutsideClick START ${this.ctxMenuId} ===`);
      console.debug(event);
      console.debug(this.anchorElementId);
      if (this.anchorElementId) {
        const anchorElement = document.querySelector(`#${this.anchorElementId}`);
        console.debug(anchorElement);
        console.debug(event.path.includes(anchorElement));
        if (event.path.includes(anchorElement)){
          console.debug(`=== emitOutsideClick CANCEL ${this.ctxMenuId} ===`);
          return;
        }
      }
      this.$emit('ctx-menu-click-outside', event, this.ctxMenuId);
      console.debug(`=== emitOutsideClick END ${this.ctxMenuId} ===`);
    },
    closePopper(event) {
      console.debug(`Closed Context Menu`);
      this.isVisible = false;
      this.contextData = null;
      this.originalEvent = null;
      console.debug(this.$parent);
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
