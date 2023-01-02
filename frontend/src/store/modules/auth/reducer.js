import * as types from '../types'
const initialState = {
    isLoggedIn: false,
    token: {},
    user: {},
    isAdmin: false,
    isLoading: false,
}

export default function (state = initialState, action) {
    switch (action.type) {
        case types.LOGIN_SUCCESS: {
            
            const newState = {...state}
            newState.isLoggedIn = true;
            if(action.payload.payload.username == 'principal'){
                newState.isAdmin = true
            }

            newState.token = action.payload.token
            newState.user = action.payload.payload.username
            
            return newState;
        }

        case types.LOGIN_FAILURE: {
            const newState = { ...initialState}
            return newState;
        }

        default: {
            return state
        }
    }
}