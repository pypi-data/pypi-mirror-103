(window.webpackJsonp=window.webpackJsonp||[]).push([[115],{1116:function(e,t,r){"use strict";r.r(t);r(45),r(11),r(41),r(42),r(19),r(20),r(113),r(10);var n=r(1),l=r(17),o=(r(9),r(7),r(142),r(18),r(55),r(177)),c=r.n(o),d=r(1083),f=r.n(d),v=(r(1085),r(1087)),m=r.n(v);function h(e,t){var r;if("undefined"==typeof Symbol||null==e[Symbol.iterator]){if(Array.isArray(e)||(r=function(e,t){if(!e)return;if("string"==typeof e)return y(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return y(e,t)}(e))||t&&e&&"number"==typeof e.length){r&&(e=r);var i=0,n=function(){};return{s:n,n:function(){return i>=e.length?{done:!0}:{done:!1,value:e[i++]}},e:function(e){throw e},f:n}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var l,o=!0,c=!1;return{s:function(){r=e[Symbol.iterator]()},n:function(){var e=r.next();return o=e.done,e},e:function(e){c=!0,l=e},f:function(){try{o||null==r.return||r.return()}finally{if(c)throw l}}}}function y(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}var _={layout:"project",components:{FilePond:f()(m.a)},data:function(){return{catalog:[],selected:null,myFiles:[],option:{column_data:"",column_label:"",delimiter:""},taskId:null,polling:null,errors:[],headers:[{text:"Filename",value:"filename"},{text:"Line",value:"line"},{text:"Message",value:"message"}],requiredRules:[function(e){return!!e||"Field value is required"}],server:{url:"/v1/fp",headers:{"X-CSRFToken":c.a.get("csrftoken")},process:{url:"/process/",method:"POST"},patch:"/patch/",revert:"/revert/",restore:"/restore/",load:"/load/",fetch:"/fetch/"},uploadedFiles:[],valid:!1}},computed:{isDisabled:function(){return 0===this.uploadedFiles.length||null!==this.taskId||!this.valid},properties:function(){var e=this,t=this.catalog.find((function(t){return t.name===e.selected}));return t?t.properties:{}},textFields:function(){var e=Object.entries(this.properties).filter((function(e){var t=Object(l.a)(e,2);t[0];return!("enum"in t[1])}));return Object.fromEntries(e)},selectFields:function(){var e=Object.entries(this.properties).filter((function(e){var t=Object(l.a)(e,2);t[0];return"enum"in t[1]}));return Object.fromEntries(e)},acceptedFileTypes:function(){var e=this,t=this.catalog.find((function(t){return t.name===e.selected}));return t?t.acceptTypes:""},example:function(){var e=this,t=this.catalog.find((function(t){return t.name===e.selected}));if(t){return"column_data"in this.option&&"column_label"in this.option?t.example.replaceAll("column_data",this.option.column_data).replaceAll("column_label",this.option.column_label).trim():t.example.trim()}return""}},watch:{selected:function(){for(var e=this,t=this.catalog.find((function(t){return t.name===e.selected})),r=0,n=Object.entries(t.properties);r<n.length;r++){var o=Object(l.a)(n[r],2),c=o[0],d=o[1];this.option[c]=d.default}this.myFiles=[];var f,v=h(this.uploadedFiles);try{for(v.s();!(f=v.n()).done;){var m=f.value;this.$services.parse.revert(m.serverId)}}catch(e){v.e(e)}finally{v.f()}this.uploadedFiles=[],this.errors=[]}},created:function(){var e=this;return Object(n.a)(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,e.$services.catalog.list(e.$route.params.id);case 2:e.catalog=t.sent,e.pollData();case 4:case"end":return t.stop()}}),t)})))()},beforeDestroy:function(){clearInterval(this.polling)},methods:{handleFilePondProcessfile:function(e,t){console.log(e),this.uploadedFiles.push(t),this.$nextTick()},handleFilePondRemovefile:function(e,t){console.log(e);var r=this.uploadedFiles.findIndex((function(e){return e.id===t.id}));r>-1&&(this.uploadedFiles.splice(r,1),this.$nextTick())},injest:function(){var e=this;return Object(n.a)(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,e.$services.parse.analyze(e.$route.params.id,e.selected,e.uploadedFiles.map((function(e){return e.serverId})),e.option);case 2:e.taskId=t.sent;case 3:case"end":return t.stop()}}),t)})))()},pollData:function(){var e=this;this.polling=setInterval(Object(n.a)(regeneratorRuntime.mark((function t(){var r;return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(!e.taskId){t.next=5;break}return t.next=3,e.$services.taskStatus.get(e.taskId);case 3:(r=t.sent).ready&&(e.taskId=null,e.errors=r.result.error,e.myFiles=[],e.uploadedFiles=[]);case 5:case"end":return t.stop()}}),t)}))),3e3)},toVisualize:function(text){return"\t"===text?"Tab":" "===text?"Space":""===text?"None":text}}},F=r(27),k=r(31),x=r.n(k),w=r(195),j=r(508),I=r(491),O=r(1104),T=r(559),V=r(176),$=r(145),S=r(555),P=r(50),R=r(533),C=r(506),component=Object(F.a)(_,(function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-card",[r("v-card-title",[e._v("\n    "+e._s(e.$t("dataset.importDataTitle"))+"\n  ")]),e._v(" "),r("v-card-text",[r("v-overlay",{attrs:{value:e.taskId}},[r("v-progress-circular",{attrs:{indeterminate:"",size:"64"}})],1),e._v(" "),r("v-select",{attrs:{items:e.catalog,"item-text":"name",label:"File format",outlined:""},model:{value:e.selected,callback:function(t){e.selected=t},expression:"selected"}}),e._v(" "),r("v-form",{model:{value:e.valid,callback:function(t){e.valid=t},expression:"valid"}},[e._l(e.textFields,(function(t,n){return r("v-text-field",{key:n,attrs:{label:t.title,rules:e.requiredRules,outlined:""},model:{value:e.option[n],callback:function(t){e.$set(e.option,n,t)},expression:"option[key]"}})})),e._v(" "),e._l(e.selectFields,(function(t,n){return r("v-select",{key:n,attrs:{items:t.enum,label:t.title,outlined:""},scopedSlots:e._u([{key:"selection",fn:function(t){var r=t.item;return[e._v("\n          "+e._s(e.toVisualize(r))+"\n        ")]}},{key:"item",fn:function(t){var r=t.item;return[e._v("\n          "+e._s(e.toVisualize(r))+"\n        ")]}}],null,!0),model:{value:e.option[n],callback:function(t){e.$set(e.option,n,t)},expression:"option[key]"}})}))],2),e._v(" "),e.selected?r("v-sheet",{staticClass:"mb-5 pa-5",attrs:{dark:!e.$vuetify.theme.dark,light:e.$vuetify.theme.dark}},[r("pre",[e._v(e._s(e.example))])]):e._e(),e._v(" "),e.selected&&"*"!==e.acceptedFileTypes?r("file-pond",{ref:"pond",attrs:{"chunk-uploads":"true","label-idle":"Drop files here...","allow-multiple":!0,"accepted-file-types":e.acceptedFileTypes,server:e.server,files:e.myFiles},on:{processfile:e.handleFilePondProcessfile,removefile:e.handleFilePondRemovefile}}):e._e(),e._v(" "),e.selected&&"*"===e.acceptedFileTypes?r("file-pond",{ref:"pond",attrs:{"chunk-uploads":"true","label-idle":"Drop files here...","allow-multiple":!0,server:e.server,files:e.myFiles},on:{processfile:e.handleFilePondProcessfile,removefile:e.handleFilePondRemovefile}}):e._e(),e._v(" "),e.errors.length>0?r("v-data-table",{staticClass:"elevation-1",attrs:{headers:e.headers,items:e.errors}}):e._e()],1),e._v(" "),r("v-card-actions",[r("v-spacer"),e._v(" "),r("v-btn",{staticClass:"text-capitalize me-2 primary",attrs:{disabled:e.isDisabled},on:{click:e.injest}},[e._v("\n      Injest\n    ")])],1)],1)}),[],!1,null,null,null);t.default=component.exports;x()(component,{VBtn:w.a,VCard:j.a,VCardActions:I.a,VCardText:I.b,VCardTitle:I.c,VDataTable:O.a,VForm:T.a,VOverlay:V.a,VProgressCircular:$.a,VSelect:S.a,VSheet:P.a,VSpacer:R.a,VTextField:C.a})}}]);