import React from 'react'
import { Switch } from 'react-router-dom'
import MyRoute from './MyRoute'
import Login from '../components/Login/Login'
import Dashboard from '../components/dashboard/Dashboard'
import Home from '../components/Home/Home'
import Carrinho from '../components/Carrinho/Carrinho'
import Page404 from '../components/Page404/Page404'
import Detail from '../components/Detail/Detail'
export default function Routes() {
    return (
        <Switch>
            <MyRoute exact path='/' component={Home} />
            <MyRoute exact path='/cart' component={Carrinho} isClosed/>
            <MyRoute exact path='/dashboard' component={Dashboard} isClosed/>
            <MyRoute exact path='/login' component={Login} isClosed={false}/>
            <MyRoute exact path='/produto/detalhes/:id' component={Detail} isClosed/>
            <MyRoute exact path='*' component={Page404} />
        </Switch>

    )
}
