import _emitter from "./emitter";
import EnumStatusLogLevel from "../constants/loglevels";

console.log(_emitter);

export function logStatus(id, logLevel, payload){
  _emitter.emit(`status-bar-log-${id}`, {logLevel, payload})
}
