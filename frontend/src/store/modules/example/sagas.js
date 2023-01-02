import {call, put, all, takeLatest } from '@redux-saga/core/effects'
import { toast } from 'react-toastify'
import * as types from '../types'
import * as act from './actions'
const requisicao = () => new Promise((resolve, reject)=>{
    setTimeout(()=>{
        resolve()
    }, 2000)
})

function* exampleRequest(){
    try{
        yield call(requisicao)
        yield put(act.clicaBotaoSuccess())
        toast.success('sucesso')
    } catch{
        
        yield put(act.clicaBotaoFailure())
    }
}

export default all([
    takeLatest(types.BOTAO_CLICADO_REQUEST, exampleRequest)
])