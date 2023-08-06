(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[2569],{86977:(e,t,r)=>{"use strict";r.d(t,{Q:()=>i});const i=e=>!(!e.detail.selected||"property"!==e.detail.source)&&(e.currentTarget.selected=!1,!0)},15493:(e,t,r)=>{"use strict";r.d(t,{Q2:()=>i,io:()=>n,ou:()=>o,j4:()=>s,pc:()=>a});const i=()=>{const e={},t=new URLSearchParams(location.search);for(const[r,i]of t.entries())e[r]=i;return e},n=e=>new URLSearchParams(window.location.search).get(e),o=e=>{const t=new URLSearchParams;return Object.entries(e).forEach((([e,r])=>{t.append(e,r)})),t.toString()},s=e=>{const t=new URLSearchParams(window.location.search);return Object.entries(e).forEach((([e,r])=>{t.set(e,r)})),t.toString()},a=e=>{const t=new URLSearchParams(window.location.search);return t.delete(e),t.toString()}},96151:(e,t,r)=>{"use strict";r.d(t,{T:()=>i,y:()=>n});const i=e=>{requestAnimationFrame((()=>setTimeout(e,0)))},n=()=>new Promise((e=>{i(e)}))},81545:(e,t,r)=>{"use strict";r(33300);var i=r(15652);function n(){n=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!a(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=d(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function o(e){var t,r=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function a(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var c=n();if(i)for(var d=0;d<i.length;d++)c=i[d](c);var f=t((function(e){c.initializeInstanceElements(e,h.elements)}),r),h=c.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(l(o.descriptor)||l(n.descriptor)){if(a(o)||a(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(a(o)){if(a(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}s(o,n)}else t.push(o)}return t}(f.d.map(o)),e);c.initializeClassElements(f.F,h.elements),c.runClassFinishers(f.F,h.finishers)}([(0,i.Mo)("ha-button-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)()],key:"corner",value:()=>"TOP_START"},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"multi",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"activatable",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,i.IO)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"render",value:function(){return i.dy`
      <div @click=${this._handleClick}>
        <slot name="trigger"></slot>
      </div>
      <mwc-menu
        .corner=${this.corner}
        .multi=${this.multi}
        .activatable=${this.activatable}
      >
        <slot></slot>
      </mwc-menu>
    `}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this,this._menu.show())}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),i.oi)},32511:(e,t,r)=>{"use strict";r(39494);var i=r(15652);function n(){n=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!a(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=d(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function o(e){var t,r=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function a(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function h(e,t,r){return(h="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=p(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function p(e){return(p=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const u=customElements.get("mwc-checkbox");!function(e,t,r,i){var c=n();if(i)for(var d=0;d<i.length;d++)c=i[d](c);var f=t((function(e){c.initializeInstanceElements(e,h.elements)}),r),h=c.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(l(o.descriptor)||l(n.descriptor)){if(a(o)||a(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(a(o)){if(a(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}s(o,n)}else t.push(o)}return t}(f.d.map(o)),e);c.initializeClassElements(f.F,h.elements),c.runClassFinishers(f.F,h.finishers)}([(0,i.Mo)("ha-checkbox")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"method",key:"firstUpdated",value:function(){h(p(r.prototype),"firstUpdated",this).call(this),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}}]}}),u)},36125:(e,t,r)=>{"use strict";r(29119);var i=r(15652);function n(){n=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!a(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=d(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function o(e){var t,r=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function a(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function h(e,t,r){return(h="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=p(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function p(e){return(p=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const u=customElements.get("mwc-fab");!function(e,t,r,i){var c=n();if(i)for(var d=0;d<i.length;d++)c=i[d](c);var f=t((function(e){c.initializeInstanceElements(e,h.elements)}),r),h=c.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(l(o.descriptor)||l(n.descriptor)){if(a(o)||a(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(a(o)){if(a(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}s(o,n)}else t.push(o)}return t}(f.d.map(o)),e);c.initializeClassElements(f.F,h.elements),c.runClassFinishers(f.F,h.finishers)}([(0,i.Mo)("ha-fab")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"method",key:"firstUpdated",value:function(e){h(p(r.prototype),"firstUpdated",this).call(this,e),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}}]}}),u)},2852:(e,t,r)=>{"use strict";r.d(t,{t:()=>c});var i=r(15652),n=r(85415),o=r(35359),s=r(73728),a=r(5986),l=r(52871);const c=(e,t)=>(0,l.w)(e,t,{loadDevicesAndAreas:!0,getFlowHandlers:async e=>{const[t]=await Promise.all([(0,s.d4)(e),e.loadBackendTranslation("title",void 0,!0)]);return t.sort(((t,r)=>(0,n.w)((0,a.Lh)(e.localize,t),(0,a.Lh)(e.localize,r))))},createFlow:async(e,t)=>{const[r]=await Promise.all([(0,s.Ky)(e,t),e.loadBackendTranslation("config",t)]);return r},fetchFlow:async(e,t)=>{const r=await(0,s.D4)(e,t);return await e.loadBackendTranslation("config",r.handler),r},handleFlowStep:s.XO,deleteFlow:s.oi,renderAbortDescription(e,t){const r=(0,o.I)(e.localize,`component.${t.handler}.config.abort.${t.reason}`,t.description_placeholders);return r?i.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderShowFormStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormStepDescription(e,t){const r=(0,o.I)(e.localize,`component.${t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return r?i.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(e,t,r)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.data.${r.name}`),renderShowFormStepFieldError:(e,t,r)=>e.localize(`component.${t.handler}.config.error.${r}`),renderExternalStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site"),renderExternalStepDescription(e,t){const r=(0,o.I)(e.localize,`component.${t.handler}.config.${t.step_id}.description`,t.description_placeholders);return i.dy`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${r?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${r}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const r=(0,o.I)(e.localize,`component.${t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return i.dy`
        ${r?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${r}
              ></ha-markdown>
            `:""}
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.created_config","name",t.title)}
        </p>
      `},renderShowFormProgressHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormProgressDescription(e,t){const r=(0,o.I)(e.localize,`component.${t.handler}.config.progress.${t.progress_action}`,t.description_placeholders);return r?i.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""}})},73826:(e,t,r)=>{"use strict";r.d(t,{f:()=>m});var i=r(15652);function n(e,t,r,i){var n=o();if(i)for(var d=0;d<i.length;d++)n=i[d](n);var f=t((function(e){n.initializeInstanceElements(e,h.elements)}),r),h=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(c(o.descriptor)||c(n.descriptor)){if(l(o)||l(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(l(o)){if(l(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}a(o,n)}else t.push(o)}return t}(f.d.map(s)),e);return n.initializeClassElements(f.F,h.elements),n.runClassFinishers(f.F,h.finishers)}function o(){o=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!l(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=f(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function s(e){var t,r=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function a(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function l(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function p(e,t,r){return(p="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=u(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function u(e){return(u=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const m=e=>n(null,(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){p(u(r.prototype),"connectedCallback",this).call(this),this.__checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if(p(u(r.prototype),"disconnectedCallback",this).call(this),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then((e=>e())):e()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(e){p(u(r.prototype),"updated",this).call(this,e),e.has("hass")&&this.__checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"__checkSubscribed",value:function(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&(this.__unsubs=this.hassSubscribe())}}]}}),e)},72569:(e,t,r)=>{"use strict";r.r(t);r(25230),r(81689);var i=r(55317),n=r(81480),o=r(15652),s=r(49629),a=r(14516),l=r(83849),c=r(85415),d=r(15493),f=r(96151),h=r(81582),p=r(73728),u=r(57292),m=r(74186),y=r(5986),v=r(2852),g=r(26765),b=r(73826),w=r(11654),k=r(29311),E=(r(7164),r(81545),r(36125),r(32511),r(52039),r(15291),r(1359),r(51095),r(53918),r(57301),r(54444),r(81471)),_=r(47181),x=r(86977);r(99282),r(22098);const P=()=>Promise.all([r.e(5906),r.e(7982),r.e(9146),r.e(3466)]).then(r.bind(r,23466));var z=r(17416),C=r(11254);function D(){D=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!S(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return F(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?F(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=j(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:O(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=O(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function $(e){var t,r=j(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function A(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function S(e){return e.decorators&&e.decorators.length}function T(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function O(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function j(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function F(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=D();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(T(o.descriptor)||T(n.descriptor)){if(S(o)||S(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(S(o)){if(S(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}A(o,n)}else t.push(o)}return t}(s.d.map($)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("ha-integration-header")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"banner",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"localizedDomainName",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"domain",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"manifest",value:void 0},{kind:"method",key:"render",value:function(){let e,t;const r=this.localizedDomainName||(0,y.Lh)(this.hass.localize,this.domain,this.manifest);this.label?(e=this.label,t=e===r?void 0:r):e=r;const n=[];return this.manifest&&(this.manifest.is_built_in||n.push([i.B3I,this.hass.localize("ui.panel.config.integrations.config_entry.provided_by_custom_integration")]),this.manifest.iot_class&&this.manifest.iot_class.startsWith("cloud_")&&n.push([i.lz4,this.hass.localize("ui.panel.config.integrations.config_entry.depends_on_cloud")])),o.dy`
      ${this.banner?o.dy`<div class="banner">
            ${this.banner}
          </div>`:""}
      <slot name="above-header"></slot>
      <div class="header">
        <img
          src=${(0,C.X)(this.domain,"icon")}
          referrerpolicy="no-referrer"
          @error=${this._onImageError}
          @load=${this._onImageLoad}
        />
        <div class="info">
          <div class="primary">${e}</div>
          ${t?o.dy`<div class="secondary">${t}</div>`:""}
        </div>
        ${0===n.length?"":o.dy`
              <div class="icons">
                ${n.map((([e,t])=>o.dy`
                    <span>
                      <ha-svg-icon .path=${e}></ha-svg-icon>
                      <paper-tooltip animation-delay="0"
                        >${t}</paper-tooltip
                      >
                    </span>
                  `))}
              </div>
            `}
      </div>
    `}},{kind:"method",key:"_onImageLoad",value:function(e){e.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(e){e.target.style.visibility="hidden"}},{kind:"field",static:!0,key:"styles",value:()=>o.iv`
    .banner {
      background-color: var(--state-color);
      color: var(--text-on-state-color);
      text-align: center;
      padding: 2px;
    }
    .header {
      display: flex;
      position: relative;
      padding: 16px 8px 8px 16px;
    }
    .header img {
      margin-right: 16px;
      width: 40px;
      height: 40px;
    }
    .header .info {
      align-self: center;
    }
    .header .info div {
      word-wrap: break-word;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .primary {
      font-size: 16px;
      font-weight: 400;
      color: var(--primary-text-color);
    }
    .secondary {
      font-size: 14px;
      color: var(--secondary-text-color);
    }
    .icons {
      position: absolute;
      top: 0px;
      right: 16px;
      color: var(--text-on-state-color, var(--secondary-text-color));
      background-color: var(--state-color, #e0e0e0);
      border-bottom-left-radius: 4px;
      border-bottom-right-radius: 4px;
      padding: 1px 4px 2px;
    }
    .icons ha-svg-icon {
      width: 20px;
      height: 20px;
    }
    paper-tooltip {
      white-space: nowrap;
    }
  `}]}}),o.oi);function I(){I=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!U(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return q(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?q(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=L(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:N(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=N(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function R(e){var t,r=L(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function M(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function U(e){return e.decorators&&e.decorators.length}function B(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function N(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function L(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function q(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}const Q=["migration_error","setup_error","setup_retry"],W={hassio:"/hassio/dashboard",mqtt:"/config/mqtt",zha:"/config/zha/dashboard",ozw:"/config/ozw/dashboard",zwave:"/config/zwave",zwave_js:"/config/zwave_js/dashboard"};!function(e,t,r,i){var n=I();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(B(o.descriptor)||B(n.descriptor)){if(U(o)||U(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(U(o)){if(U(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}M(o,n)}else t.push(o)}return t}(s.d.map(R)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("ha-integration-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"domain",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"items",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"manifest",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"entityRegistryEntries",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"deviceRegistryEntries",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"selectedConfigEntryId",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"method",key:"render",value:function(){let e=this._selectededConfigEntry;1===this.items.length?e=this.items[0]:this.selectedConfigEntryId&&(e=this.items.find((e=>e.entry_id===this.selectedConfigEntryId)));const t=void 0!==e;return o.dy`
      <ha-card
        outlined
        class="${(0,E.$)({single:t,group:!t,hasMultiple:this.items.length>1,disabled:this.disabled,"state-not-loaded":t&&"not_loaded"===e.state,"state-failed-unload":t&&"failed_unload"===e.state,"state-error":t&&Q.includes(e.state)})}"
        .configEntry=${e}
      >
        <ha-integration-header
          .hass=${this.hass}
          .banner=${this.disabled?this.hass.localize("ui.panel.config.integrations.config_entry.disable.disabled"):void 0}
          .domain=${this.domain}
          .label=${e?e.title||e.localized_domain_name||this.domain:void 0}
          .localizedDomainName=${e?e.localized_domain_name:void 0}
          .manifest=${this.manifest}
        >
          ${this.items.length>1?o.dy`
                <div class="back-btn" slot="above-header">
                  <ha-icon-button
                    icon="hass:chevron-left"
                    @click=${this._back}
                  ></ha-icon-button>
                </div>
              `:""}
        </ha-integration-header>

        ${e?this._renderSingleEntry(e):this._renderGroupedIntegration()}
      </ha-card>
    `}},{kind:"method",key:"_renderGroupedIntegration",value:function(){return o.dy`
      <paper-listbox>
        ${this.items.map((e=>o.dy`<paper-item
              .entryId=${e.entry_id}
              @click=${this._selectConfigEntry}
              ><paper-item-body
                >${e.title||this.hass.localize("ui.panel.config.integrations.config_entry.unnamed_entry")}</paper-item-body
              >
              ${Q.includes(e.state)?o.dy`<span>
                    <ha-svg-icon
                      class="error"
                      .path=${i.fr4}
                    ></ha-svg-icon
                    ><paper-tooltip animation-delay="0" position="left">
                      ${this.hass.localize(`ui.panel.config.integrations.config_entry.state.${e.state}`)}
                    </paper-tooltip>
                  </span>`:""}
              <ha-icon-next></ha-icon-next>
            </paper-item>`))}
      </paper-listbox>
    `}},{kind:"method",key:"_renderSingleEntry",value:function(e){const t=this._getDevices(e),r=this._getServices(e),n=this._getEntities(e);let s,a;return e.disabled_by?(s=["ui.panel.config.integrations.config_entry.disable.disabled_cause","cause",this.hass.localize(`ui.panel.config.integrations.config_entry.disable.disabled_by.${e.disabled_by}`)||e.disabled_by],"failed_unload"===e.state&&(a=o.dy`.
        ${this.hass.localize("ui.panel.config.integrations.config_entry.disable_restart_confirm")}.`)):"not_loaded"===e.state?s=["ui.panel.config.integrations.config_entry.not_loaded"]:Q.includes(e.state)&&(s=[`ui.panel.config.integrations.config_entry.state.${e.state}`],e.reason?(this.hass.loadBackendTranslation("config",e.domain),a=o.dy`:
        ${this.hass.localize(`component.${e.domain}.config.error.${e.reason}`)||e.reason}`):a=o.dy`
          <br />
          <a href="/config/logs"
            >${this.hass.localize("ui.panel.config.integrations.config_entry.check_the_logs")}</a
          >
        `),o.dy`
      ${s?o.dy`
            <div class="message">
              <ha-svg-icon .path=${i.fr4}></ha-svg-icon>
              <div>
                ${this.hass.localize(...s)}${a}
              </div>
            </div>
          `:""}
      <div class="content">
        ${t.length||r.length||n.length?o.dy`
              <div>
                ${t.length?o.dy`
                      <a
                        href=${`/config/devices/dashboard?historyBack=1&config_entry=${e.entry_id}`}
                        >${this.hass.localize("ui.panel.config.integrations.config_entry.devices","count",t.length)}</a
                      >${r.length?",":""}
                    `:""}
                ${r.length?o.dy`
                      <a
                        href=${`/config/devices/dashboard?historyBack=1&config_entry=${e.entry_id}`}
                        >${this.hass.localize("ui.panel.config.integrations.config_entry.services","count",r.length)}</a
                      >
                    `:""}
                ${(t.length||r.length)&&n.length?this.hass.localize("ui.common.and"):""}
                ${n.length?o.dy`
                      <a
                        href=${`/config/entities?historyBack=1&config_entry=${e.entry_id}`}
                        >${this.hass.localize("ui.panel.config.integrations.config_entry.entities","count",n.length)}</a
                      >
                    `:""}
              </div>
            `:""}
      </div>
      <div class="actions">
        <div>
          ${"user"===e.disabled_by?o.dy`<mwc-button unelevated @click=${this._handleEnable}>
                ${this.hass.localize("ui.common.enable")}
              </mwc-button>`:e.domain in W?o.dy`<a
                href=${`${W[e.domain]}?config_entry=${e.entry_id}`}
                ><mwc-button>
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.configure")}
                </mwc-button></a
              >`:e.supports_options?o.dy`
                <mwc-button @click=${this._showOptions}>
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.configure")}
                </mwc-button>
              `:""}
        </div>
        ${this.manifest?o.dy`
              <ha-button-menu corner="BOTTOM_START">
                <mwc-icon-button
                  .title=${this.hass.localize("ui.common.menu")}
                  .label=${this.hass.localize("ui.common.overflow_menu")}
                  slot="trigger"
                >
                  <ha-svg-icon .path=${i.SXi}></ha-svg-icon>
                </mwc-icon-button>
                <mwc-list-item @request-selected="${this._editEntryName}">
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.rename")}
                </mwc-list-item>
                <mwc-list-item @request-selected="${this._handleSystemOptions}">
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.system_options")}
                </mwc-list-item>

                <a
                  href=${this.manifest.documentation}
                  rel="noreferrer"
                  target="_blank"
                >
                  <mwc-list-item hasMeta>
                    ${this.hass.localize("ui.panel.config.integrations.config_entry.documentation")}<ha-svg-icon
                      slot="meta"
                      .path=${i.fOx}
                    ></ha-svg-icon>
                  </mwc-list-item>
                </a>
                ${!e.disabled_by&&"loaded"===e.state&&e.supports_unload&&"system"!==e.source?o.dy`<mwc-list-item
                      @request-selected="${this._handleReload}"
                    >
                      ${this.hass.localize("ui.panel.config.integrations.config_entry.reload")}
                    </mwc-list-item>`:""}
                ${"user"===e.disabled_by?o.dy`<mwc-list-item
                      @request-selected="${this._handleEnable}"
                    >
                      ${this.hass.localize("ui.common.enable")}
                    </mwc-list-item>`:"system"!==e.source?o.dy`<mwc-list-item
                      class="warning"
                      @request-selected="${this._handleDisable}"
                    >
                      ${this.hass.localize("ui.common.disable")}
                    </mwc-list-item>`:""}
                ${"system"!==e.source?o.dy`<mwc-list-item
                      class="warning"
                      @request-selected="${this._handleDelete}"
                    >
                      ${this.hass.localize("ui.panel.config.integrations.config_entry.delete")}
                    </mwc-list-item>`:""}
              </ha-button-menu>
            `:""}
      </div>
    `}},{kind:"get",key:"_selectededConfigEntry",value:function(){return 1===this.items.length?this.items[0]:this.selectedConfigEntryId?this.items.find((e=>e.entry_id===this.selectedConfigEntryId)):void 0}},{kind:"method",key:"_selectConfigEntry",value:function(e){this.selectedConfigEntryId=e.currentTarget.entryId}},{kind:"method",key:"_back",value:function(){this.selectedConfigEntryId=void 0,this.classList.remove("highlight")}},{kind:"method",key:"_getEntities",value:function(e){return this.entityRegistryEntries?this.entityRegistryEntries.filter((t=>t.config_entry_id===e.entry_id)):[]}},{kind:"method",key:"_getDevices",value:function(e){return this.deviceRegistryEntries?this.deviceRegistryEntries.filter((t=>t.config_entries.includes(e.entry_id)&&"service"!==t.entry_type)):[]}},{kind:"method",key:"_getServices",value:function(e){return this.deviceRegistryEntries?this.deviceRegistryEntries.filter((t=>t.config_entries.includes(e.entry_id)&&"service"===t.entry_type)):[]}},{kind:"method",key:"_showOptions",value:function(e){(0,z.c)(this,e.target.closest("ha-card").configEntry)}},{kind:"method",key:"_handleReload",value:function(e){(0,x.Q)(e)&&this._reloadIntegration(e.target.closest("ha-card").configEntry)}},{kind:"method",key:"_handleDelete",value:function(e){(0,x.Q)(e)&&this._removeIntegration(e.target.closest("ha-card").configEntry)}},{kind:"method",key:"_handleDisable",value:function(e){(0,x.Q)(e)&&this._disableIntegration(e.target.closest("ha-card").configEntry)}},{kind:"method",key:"_handleEnable",value:function(e){e.detail.source&&!(0,x.Q)(e)||this._enableIntegration(e.target.closest("ha-card").configEntry)}},{kind:"method",key:"_handleSystemOptions",value:function(e){(0,x.Q)(e)&&this._showSystemOptions(e.target.closest("ha-card").configEntry)}},{kind:"method",key:"_showSystemOptions",value:function(e){var t,r;t=this,r={entry:e},(0,_.B)(t,"show-dialog",{dialogTag:"dialog-config-entry-system-options",dialogImport:P,dialogParams:r})}},{kind:"method",key:"_disableIntegration",value:async function(e){const t=e.entry_id;if(!await(0,g.g7)(this,{text:this.hass.localize("ui.panel.config.integrations.config_entry.disable.disable_confirm")}))return;(await(0,h.Ny)(this.hass,t)).require_restart&&(0,g.Ys)(this,{text:this.hass.localize("ui.panel.config.integrations.config_entry.disable_restart_confirm")}),(0,_.B)(this,"entry-updated",{entry:{...e,disabled_by:"user"}})}},{kind:"method",key:"_enableIntegration",value:async function(e){const t=e.entry_id;(await(0,h.T0)(this.hass,t)).require_restart&&(0,g.Ys)(this,{text:this.hass.localize("ui.panel.config.integrations.config_entry.enable_restart_confirm")}),(0,_.B)(this,"entry-updated",{entry:{...e,disabled_by:null}})}},{kind:"method",key:"_removeIntegration",value:async function(e){const t=e.entry_id;if(!await(0,g.g7)(this,{text:this.hass.localize("ui.panel.config.integrations.config_entry.delete_confirm")}))return;const r=await(0,h.iJ)(this.hass,t);(0,_.B)(this,"entry-removed",{entryId:t}),r.require_restart&&(0,g.Ys)(this,{text:this.hass.localize("ui.panel.config.integrations.config_entry.restart_confirm")})}},{kind:"method",key:"_reloadIntegration",value:async function(e){const t=e.entry_id,r=(await(0,h.Nn)(this.hass,t)).require_restart?"reload_restart_confirm":"reload_confirm";(0,g.Ys)(this,{text:this.hass.localize(`ui.panel.config.integrations.config_entry.${r}`)})}},{kind:"method",key:"_editEntryName",value:async function(e){const t=e.target.closest("ha-card").configEntry,r=await(0,g.D9)(this,{title:this.hass.localize("ui.panel.config.integrations.rename_dialog"),defaultValue:t.title,inputLabel:this.hass.localize("ui.panel.config.integrations.rename_input_label")});if(null===r)return;const i=await(0,h.SO)(this.hass,t.entry_id,{title:r});(0,_.B)(this,"entry-updated",{entry:i})}},{kind:"get",static:!0,key:"styles",value:function(){return[w.Qx,o.iv`
        ha-card {
          display: flex;
          flex-direction: column;
          height: 100%;
          --state-color: var(--divider-color, #e0e0e0);
          --ha-card-border-color: var(--state-color);
          --state-message-color: var(--state-color);
        }
        .state-error {
          --state-color: var(--error-color);
          --text-on-state-color: var(--text-primary-color);
        }
        .state-failed-unload {
          --state-color: var(--warning-color);
          --text-on-state-color: var(--primary-text-color);
        }
        .state-not-loaded {
          --state-message-color: var(--primary-text-color);
        }
        :host(.highlight) ha-card {
          --state-color: var(--primary-color);
          --text-on-state-color: var(--text-primary-color);
        }

        .back-btn {
          background-color: var(--state-color);
          color: var(--text-on-state-color);
          --mdc-icon-button-size: 32px;
          transition: height 0.1s;
          overflow: hidden;
        }
        .hasMultiple.single .back-btn {
          height: 24px;
          display: flex;
          align-items: center;
        }
        .hasMultiple.group .back-btn {
          height: 0px;
        }

        .message {
          font-weight: bold;
          padding-bottom: 16px;
          display: flex;
          margin-left: 40px;
        }
        .message ha-svg-icon {
          color: var(--state-message-color);
        }
        .message div {
          flex: 1;
          margin-left: 8px;
          padding-top: 2px;
        }

        .content {
          flex: 1;
          padding: 0px 16px 0 72px;
        }

        .actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 8px 0 0 8px;
          height: 48px;
        }
        .actions a {
          text-decoration: none;
        }
        a {
          color: var(--primary-color);
        }
        ha-button-menu {
          color: var(--secondary-text-color);
          --mdc-menu-min-width: 200px;
        }
        @media (min-width: 563px) {
          ha-card.group {
            position: relative;
            min-height: 164px;
          }
          paper-listbox {
            position: absolute;
            top: 64px;
            left: 0;
            right: 0;
            bottom: 0;
            overflow: auto;
          }
          .disabled paper-listbox {
            top: 88px;
          }
        }
        paper-item {
          cursor: pointer;
          min-height: 35px;
        }
        paper-item-body {
          word-wrap: break-word;
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 2;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        mwc-list-item ha-svg-icon {
          color: var(--secondary-text-color);
        }
      `]}}]}}),o.oi);function Z(){Z=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!V(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return K(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?K(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=J(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:Y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=Y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function H(e){var t,r=J(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function G(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function V(e){return e.decorators&&e.decorators.length}function X(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function Y(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function J(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function K(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=Z();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(X(o.descriptor)||X(n.descriptor)){if(V(o)||V(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(V(o)){if(V(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}G(o,n)}else t.push(o)}return t}(s.d.map(H)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("ha-integration-action-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"banner",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"localizedDomainName",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"domain",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"manifest",value:void 0},{kind:"method",key:"render",value:function(){return o.dy`
      <ha-card outlined>
        <ha-integration-header
          .hass=${this.hass}
          .banner=${this.banner}
          .domain=${this.domain}
          .label=${this.label}
          .localizedDomainName=${this.localizedDomainName}
          .manifest=${this.manifest}
        ></ha-integration-header>
        <div class="filler"></div>
        <div class="actions"><slot></slot></div>
      </ha-card>
    `}},{kind:"field",static:!0,key:"styles",value:()=>o.iv`
    ha-card {
      display: flex;
      flex-direction: column;
      height: 100%;
      --ha-card-border-color: var(--state-color);
      --mdc-theme-primary: var(--state-color);
    }
    .filler {
      flex: 1;
    }
    .attention {
      --state-color: var(--error-color);
      --text-on-state-color: var(--text-primary-color);
    }
    .discovered {
      --state-color: var(--primary-color);
      --text-on-state-color: var(--text-primary-color);
    }
    .actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 6px 0;
      height: 48px;
    }
  `}]}}),o.oi);function ee(){ee=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!ie(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return ae(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?ae(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=se(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:oe(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=oe(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function te(e){var t,r=se(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function re(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function ie(e){return e.decorators&&e.decorators.length}function ne(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function oe(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function se(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function ae(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=ee();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(ne(o.descriptor)||ne(n.descriptor)){if(ie(o)||ie(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(ie(o)){if(ie(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}re(o,n)}else t.push(o)}return t}(s.d.map(te)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("ha-config-flow-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"flow",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"manifest",value:void 0},{kind:"method",key:"render",value:function(){const e=p.P3.includes(this.flow.context.source);return o.dy`
      <ha-integration-action-card
        class=${(0,E.$)({discovered:!e,attention:e})}
        .hass=${this.hass}
        .manifest=${this.manifest}
        .banner=${this.hass.localize("ui.panel.config.integrations."+(e?"attention":"discovered"))}
        .domain=${this.flow.handler}
        .label=${this.flow.localized_title}
      >
        <mwc-button
          unelevated
          @click=${this._continueFlow}
          .label=${this.hass.localize("ui.panel.config.integrations."+(e?"reconfigure":"configure"))}
        ></mwc-button>
        ${p.pV.includes(this.flow.context.source)&&this.flow.context.unique_id?o.dy`
              <mwc-button
                @click=${this._ignoreFlow}
                .label=${this.hass.localize("ui.panel.config.integrations.ignore.ignore")}
              ></mwc-button>
            `:""}
      </ha-integration-action-card>
    `}},{kind:"method",key:"_continueFlow",value:function(){(0,v.t)(this,{continueFlowId:this.flow.flow_id,dialogClosedCallback:()=>{this._handleFlowUpdated()}})}},{kind:"method",key:"_ignoreFlow",value:async function(){await(0,g.g7)(this,{title:this.hass.localize("ui.panel.config.integrations.ignore.confirm_ignore_title","name",(0,p.WW)(this.hass.localize,this.flow)),text:this.hass.localize("ui.panel.config.integrations.ignore.confirm_ignore"),confirmText:this.hass.localize("ui.panel.config.integrations.ignore.ignore")})&&(await(0,p.zO)(this.hass,this.flow.flow_id,(0,p.WW)(this.hass.localize,this.flow)),this._handleFlowUpdated())}},{kind:"method",key:"_handleFlowUpdated",value:function(){(0,_.B)(this,"change",void 0,{bubbles:!1})}},{kind:"field",static:!0,key:"styles",value:()=>o.iv`
    .attention {
      --state-color: var(--error-color);
      --text-on-state-color: var(--text-primary-color);
    }
    .discovered {
      --state-color: var(--primary-color);
      --text-on-state-color: var(--text-primary-color);
    }
  `}]}}),o.oi);function le(){le=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!fe(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return me(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?me(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=ue(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:pe(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=pe(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function ce(e){var t,r=ue(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function de(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function fe(e){return e.decorators&&e.decorators.length}function he(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function pe(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function ue(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function me(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=le();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(he(o.descriptor)||he(n.descriptor)){if(fe(o)||fe(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(fe(o)){if(fe(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}de(o,n)}else t.push(o)}return t}(s.d.map(ce)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("ha-ignored-config-entry-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"entry",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"manifest",value:void 0},{kind:"method",key:"render",value:function(){return o.dy`
      <ha-integration-action-card
        .hass=${this.hass}
        .manifest=${this.manifest}
        .banner=${this.hass.localize("ui.panel.config.integrations.ignore.ignored")}
        .domain=${this.entry.domain}
        .localizedDomainName=${this.entry.localized_domain_name}
        .label=${"Ignored"===this.entry.title?this.entry.localized_domain_name:this.entry.title}
      >
        <mwc-button
          @click=${this._removeIgnoredIntegration}
          .label=${this.hass.localize("ui.panel.config.integrations.ignore.stop_ignore")}
        ></mwc-button>
      </ha-integration-action-card>
    `}},{kind:"method",key:"_removeIgnoredIntegration",value:async function(){(0,g.g7)(this,{title:this.hass.localize("ui.panel.config.integrations.ignore.confirm_delete_ignore_title","name",this.hass.localize(`component.${this.entry.domain}.title`)),text:this.hass.localize("ui.panel.config.integrations.ignore.confirm_delete_ignore"),confirmText:this.hass.localize("ui.panel.config.integrations.ignore.stop_ignore"),confirm:async()=>{(await(0,h.iJ)(this.hass,this.entry.entry_id)).require_restart&&alert(this.hass.localize("ui.panel.config.integrations.config_entry.restart_confirm")),(0,_.B)(this,"change",void 0,{bubbles:!1})}})}},{kind:"field",static:!0,key:"styles",value:()=>o.iv`
    :host {
      --state-color: var(--divider-color, #e0e0e0);
    }

    mwc-button {
      --mdc-theme-primary: var(--primary-color);
    }
  `}]}}),o.oi);function ye(){ye=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!be(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _e(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?_e(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=Ee(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:ke(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=ke(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function ve(e){var t,r=Ee(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function ge(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function be(e){return e.decorators&&e.decorators.length}function we(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function ke(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function Ee(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function _e(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function xe(e,t,r){return(xe="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=Pe(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function Pe(e){return(Pe=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const ze=e=>{const t=new Map;return e.forEach((e=>{t.has(e.domain)?t.get(e.domain).push(e):t.set(e.domain,[e])})),t};!function(e,t,r,i){var n=ye();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(we(o.descriptor)||we(n.descriptor)){if(be(o)||be(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(be(o)){if(be(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}ge(o,n)}else t.push(o)}return t}(s.d.map(ve)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("ha-config-integrations")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"isWide",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"showAdvanced",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,o.sz)()],key:"_configEntries",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"_configEntriesInProgress",value:()=>[]},{kind:"field",decorators:[(0,o.sz)()],key:"_entityRegistryEntries",value:()=>[]},{kind:"field",decorators:[(0,o.sz)()],key:"_deviceRegistryEntries",value:()=>[]},{kind:"field",decorators:[(0,o.sz)()],key:"_manifests",value:()=>({})},{kind:"field",key:"_extraFetchedManifests",value:void 0},{kind:"field",decorators:[(0,o.sz)()],key:"_showIgnored",value:()=>!1},{kind:"field",decorators:[(0,o.sz)()],key:"_showDisabled",value:()=>!1},{kind:"field",decorators:[(0,o.sz)()],key:"_searchParms",value:()=>new URLSearchParams(window.location.hash.substring(1))},{kind:"field",decorators:[(0,o.sz)()],key:"_filter",value:void 0},{kind:"method",key:"hassSubscribe",value:function(){return[(0,m.LM)(this.hass.connection,(e=>{this._entityRegistryEntries=e})),(0,u.q4)(this.hass.connection,(e=>{this._deviceRegistryEntries=e})),(0,p.V3)(this.hass,(async e=>{const t=[];e.forEach((e=>{e.context.title_placeholders&&t.push(this.hass.loadBackendTranslation("config",e.handler)),this._fetchManifest(e.handler)})),await Promise.all(t),await(0,f.y)(),this._configEntriesInProgress=e.map((e=>({...e,localized_title:(0,p.WW)(this.hass.localize,e)})))}))]}},{kind:"field",key:"_filterConfigEntries",value:()=>(0,a.Z)(((e,t)=>{if(!t)return[...e];return new n.Z(e,{keys:["domain","localized_domain_name","title"],isCaseSensitive:!1,minMatchCharLength:2,threshold:.2}).search(t).map((e=>e.item))}))},{kind:"field",key:"_filterGroupConfigEntries",value(){return(0,a.Z)(((e,t)=>{const r=this._filterConfigEntries(e,t),i=[],n=[];for(let e=r.length-1;e>=0;e--)"ignore"===r[e].source?i.push(r.splice(e,1)[0]):null!==r[e].disabled_by&&n.push(r.splice(e,1)[0]);return[ze(r),i,ze(n)]}))}},{kind:"field",key:"_filterConfigEntriesInProgress",value:()=>(0,a.Z)(((e,t)=>{if(!t)return e;return new n.Z(e,{keys:["handler","localized_title"],isCaseSensitive:!1,minMatchCharLength:2,threshold:.2}).search(t).map((e=>e.item))}))},{kind:"method",key:"firstUpdated",value:function(e){xe(Pe(r.prototype),"firstUpdated",this).call(this,e),this._loadConfigEntries();const t=this.hass.loadBackendTranslation("title",void 0,!0);this._fetchManifests(),"/add"===this.route.path&&this._handleAdd(t)}},{kind:"method",key:"updated",value:function(e){xe(Pe(r.prototype),"updated",this).call(this,e),this._searchParms.has("config_entry")&&e.has("_configEntries")&&!e.get("_configEntries")&&this._configEntries&&this._highlightEntry()}},{kind:"method",key:"render",value:function(){if(!this._configEntries)return o.dy`<hass-loading-screen></hass-loading-screen>`;const[e,t,r]=this._filterGroupConfigEntries(this._configEntries,this._filter),n=this._filterConfigEntriesInProgress(this._configEntriesInProgress,this._filter),a=o.dy`<ha-button-menu
      corner="BOTTOM_START"
      multi
      slot=${(0,s.o)(this.narrow?"toolbar-icon":void 0)}
      @action=${this._handleMenuAction}
    >
      <mwc-icon-button
        .title=${this.hass.localize("ui.common.menu")}
        .label=${this.hass.localize("ui.common.overflow_menu")}
        slot="trigger"
      >
        <ha-svg-icon .path=${i.ghd}></ha-svg-icon>
      </mwc-icon-button>
      <mwc-list-item graphic="control" .selected=${this._showIgnored}>
        <ha-checkbox slot="graphic" .checked=${this._showIgnored}></ha-checkbox>
        ${this.hass.localize("ui.panel.config.integrations.ignore.show_ignored")}
      </mwc-list-item>
      <mwc-list-item graphic="control" .selected=${this._showDisabled}>
        <ha-checkbox
          slot="graphic"
          .checked=${this._showDisabled}
        ></ha-checkbox>
        ${this.hass.localize("ui.panel.config.integrations.disable.show_disabled")}
      </mwc-list-item>
    </ha-button-menu>`;return o.dy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        back-path="/config"
        .route=${this.route}
        .tabs=${k.configSections.integrations}
      >
        ${this.narrow?o.dy`
              <div slot="header">
                <search-input
                  .filter=${this._filter}
                  class="header"
                  no-label-float
                  no-underline
                  @value-changed=${this._handleSearchChange}
                  .label=${this.hass.localize("ui.panel.config.integrations.search")}
                ></search-input>
              </div>
              ${a}
            `:o.dy`
              <div class="search">
                <search-input
                  no-label-float
                  no-underline
                  .filter=${this._filter}
                  @value-changed=${this._handleSearchChange}
                  .label=${this.hass.localize("ui.panel.config.integrations.search")}
                ></search-input>
                ${!this._showDisabled&&r.size?o.dy`<div class="active-filters">
                      ${this.hass.localize("ui.panel.config.integrations.disable.disabled_integrations","number",r.size)}
                      <mwc-button
                        @click=${this._toggleShowDisabled}
                        .label=${this.hass.localize("ui.panel.config.integrations.disable.show")}
                      ></mwc-button>
                    </div>`:""}
                ${a}
              </div>
            `}

        <div
          class="container"
          @entry-removed=${this._handleEntryRemoved}
          @entry-updated=${this._handleEntryUpdated}
        >
          ${this._showIgnored?t.map((e=>o.dy`
                  <ha-ignored-config-entry-card
                    .hass=${this.hass}
                    .manifest=${this._manifests[e.domain]}
                    .entry=${e}
                    @change=${this._handleFlowUpdated}
                  ></ha-ignored-config-entry-card>
                `)):""}
          ${n.length?n.map((e=>o.dy`
                  <ha-config-flow-card
                    .hass=${this.hass}
                    .manifest=${this._manifests[e.handler]}
                    .flow=${e}
                    @change=${this._handleFlowUpdated}
                  ></ha-config-flow-card>
                `)):""}
          ${this._showDisabled?Array.from(r.entries()).map((([e,t])=>o.dy`<ha-integration-card
                    data-domain=${e}
                    disabled
                    .hass=${this.hass}
                    .domain=${e}
                    .items=${t}
                    .manifest=${this._manifests[e]}
                    .entityRegistryEntries=${this._entityRegistryEntries}
                    .deviceRegistryEntries=${this._deviceRegistryEntries}
                  ></ha-integration-card> `)):""}
          ${e.size?Array.from(e.entries()).map((([e,t])=>o.dy`<ha-integration-card
                    data-domain=${e}
                    .hass=${this.hass}
                    .domain=${e}
                    .items=${t}
                    .manifest=${this._manifests[e]}
                    .entityRegistryEntries=${this._entityRegistryEntries}
                    .deviceRegistryEntries=${this._deviceRegistryEntries}
                  ></ha-integration-card>`)):this._showIgnored&&0!==t.length||this._showDisabled&&0!==r.size||0!==e.size?"":o.dy`
                <div class="empty-message">
                  <h1>
                    ${this.hass.localize("ui.panel.config.integrations.none")}
                  </h1>
                  <p>
                    ${this.hass.localize("ui.panel.config.integrations.no_integrations")}
                  </p>
                  <mwc-button
                    @click=${this._createFlow}
                    unelevated
                    .label=${this.hass.localize("ui.panel.config.integrations.add_integration")}
                  ></mwc-button>
                </div>
              `}
          ${this._filter&&!n.length&&!e.size&&this._configEntries.length?o.dy`
                <div class="empty-message">
                  <h1>
                    ${this.hass.localize("ui.panel.config.integrations.none_found")}
                  </h1>
                  <p>
                    ${this.hass.localize("ui.panel.config.integrations.none_found_detail")}
                  </p>
                </div>
              `:""}
        </div>
        <ha-fab
          slot="fab"
          .label=${this.hass.localize("ui.panel.config.integrations.add_integration")}
          extended
          @click=${this._createFlow}
        >
          <ha-svg-icon slot="icon" .path=${i.qX5}></ha-svg-icon>
        </ha-fab>
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_loadConfigEntries",value:function(){(0,h.pB)(this.hass).then((e=>{this._configEntries=e.map((e=>({...e,localized_domain_name:(0,y.Lh)(this.hass.localize,e.domain)}))).sort(((e,t)=>(0,c.w)(e.localized_domain_name+e.title,t.localized_domain_name+t.title)))}))}},{kind:"method",key:"_fetchManifests",value:async function(){const e=await(0,y.F3)(this.hass),t={...this._manifests};for(const r of e)t[r.domain]=r;this._manifests=t}},{kind:"method",key:"_fetchManifest",value:async function(e){if(e in this._manifests)return;if(this._extraFetchedManifests){if(this._extraFetchedManifests.has(e))return}else this._extraFetchedManifests=new Set;this._extraFetchedManifests.add(e);const t=await(0,y.t4)(this.hass,e);this._manifests={...this._manifests,[e]:t}}},{kind:"method",key:"_handleEntryRemoved",value:function(e){this._configEntries=this._configEntries.filter((t=>t.entry_id!==e.detail.entryId))}},{kind:"method",key:"_handleEntryUpdated",value:function(e){const t=e.detail.entry;this._configEntries=this._configEntries.map((e=>e.entry_id===t.entry_id?{...t,localized_domain_name:e.localized_domain_name}:e))}},{kind:"method",key:"_handleFlowUpdated",value:function(){this._loadConfigEntries(),(0,p.ZJ)(this.hass.connection).refresh(),this._fetchManifests()}},{kind:"method",key:"_createFlow",value:function(){(0,v.t)(this,{dialogClosedCallback:()=>{this._handleFlowUpdated()},showAdvanced:this.showAdvanced}),this.hass.loadBackendTranslation("title",void 0,!0)}},{kind:"method",key:"_handleMenuAction",value:function(e){switch(e.detail.index){case 0:this._showIgnored=!this._showIgnored;break;case 1:this._toggleShowDisabled()}}},{kind:"method",key:"_toggleShowDisabled",value:function(){this._showDisabled=!this._showDisabled}},{kind:"method",key:"_handleSearchChange",value:function(e){this._filter=e.detail.value}},{kind:"method",key:"_highlightEntry",value:async function(){await(0,f.y)();const e=this._searchParms.get("config_entry"),t=this._configEntries.find((t=>t.entry_id===e));if(!t)return;const r=this.shadowRoot.querySelector(`[data-domain=${null==t?void 0:t.domain}]`);r&&(r.scrollIntoView({block:"center"}),r.classList.add("highlight"),r.selectedConfigEntryId=e)}},{kind:"method",key:"_handleAdd",value:async function(e){var t;const r=(0,d.io)("domain");if((0,l.c)(this,"/config/integrations",!0),!r)return;const i=await e;await(0,g.g7)(this,{title:i("ui.panel.config.integrations.confirm_new","integration",(0,y.Lh)(i,r))})&&(0,v.t)(this,{dialogClosedCallback:()=>{this._handleFlowUpdated()},startFlowHandler:r,showAdvanced:null===(t=this.hass.userData)||void 0===t?void 0:t.showAdvanced})}},{kind:"get",static:!0,key:"styles",value:function(){return[w.Qx,o.iv`
        ha-button-menu {
          margin: 0 -8px 0 8px;
        }
        .container {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          grid-gap: 16px 16px;
          padding: 8px 16px 16px;
          margin-bottom: 64px;
        }
        .container > * {
          max-width: 500px;
        }

        .empty-message {
          margin: auto;
          text-align: center;
        }
        .empty-message h1 {
          margin-bottom: 0;
        }

        search-input.header {
          display: block;
          position: relative;
          left: -8px;
          color: var(--secondary-text-color);
          margin-left: 16px;
        }
        .search {
          display: flex;
          align-items: center;
          padding: 0 16px;
          background: var(--sidebar-background-color);
          border-bottom: 1px solid var(--divider-color);
        }
        .search search-input {
          flex: 1;
          position: relative;
          top: 2px;
        }

        .active-filters {
          color: var(--primary-text-color);
          position: relative;
          display: flex;
          align-items: center;
          padding: 2px 2px 2px 8px;
          margin-left: 4px;
          font-size: 14px;
        }
        .active-filters ha-icon {
          color: var(--primary-color);
        }
        .active-filters mwc-button {
          margin-left: 8px;
        }
        .active-filters::before {
          background-color: var(--primary-color);
          opacity: 0.12;
          border-radius: 4px;
          position: absolute;
          top: 0;
          right: 0;
          bottom: 0;
          left: 0;
          content: "";
        }
      `]}}]}}),(0,b.f)(o.oi))}}]);
//# sourceMappingURL=chunk.9ccd840cd602281ebd02.js.map