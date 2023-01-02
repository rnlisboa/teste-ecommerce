import {call, put, all, takeLatest } from '@redux-saga/core/effects'
import { toast } from 'react-toastify'
import * as types from '../types'
import * as act from './actions'
import axios from '../../../services/axios'
import history from '../../../services/history'
import {get} from 'lodash'
function* loginRequest({payload}){
    try{
        
        const response = yield call(axios.post,'/token/', payload);
        let data = {payload, token: response.data.access}
        
        yield put(act.loginSuccess(data))

        toast.success('Login realizado com sucesso.')

        axios.defaults.headers.Authorization = `Bearer ${response.data.access}`
        history.push(payload.prevPath)
    } catch(e){
        toast.error('Usuário ou senha inválidos.')
        yield put(act.loginFailure)
    }

    
}

function persistRehydrate({payload}){
    const token = get(payload, 'auth.token', '')
    if(!token) return
    axios.defaults.headers.Authorization = `Bearer ${token}`
}

export default all([
    takeLatest(types.LOGIN_REQUEST, loginRequest),
    takeLatest(types.PERSIST_REHYDRATE, persistRehydrate)
])