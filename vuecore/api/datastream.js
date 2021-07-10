
import { EOL } from 'os';
import { Transform } from 'stream'

/*
* Takes in a string stream and emits batches seperated by newlines
* Reference: https://github.com/extrabacon/python-shell/blob/master/index.ts#L73
*/
export class NewlineTransformer extends Transform {
    // NewlineTransformer: Megatron's little known once-removed cousin
    _lastLineData;
    _transform(chunk, encoding, callback){
        let data = chunk.toString()
        if (this._lastLineData) data = this._lastLineData + data
        const lines = data.split(EOL)
        this._lastLineData = lines.pop()
        //@ts-ignore this works, node ignores the encoding if it's a number
        lines.forEach(this.push.bind(this))
        callback()
    }
    _flush(done){
        if (this._lastLineData) this.push(this._lastLineData)
        this._lastLineData = null;
        done()
    }
}
