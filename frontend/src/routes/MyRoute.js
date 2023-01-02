import React from "react";
import {Redirect, Route } from "react-router-dom";
import PropTypes from 'prop-types'
import { useSelector } from "react-redux";
export default function MyRoute({component: Component, isClosed, onlyAdmin,...rest}){
    const isLoggedIn = useSelector(state => state.auth.isLoggedIn);
    const isAdmin = useSelector(state => state.auth.isAdmin)
    if (isClosed && !isLoggedIn){
        return (
            <Redirect 
                to={{
                    pathname: '/login', 
                    state: {prevPath: rest.location.pathname}
                }}
            />
        );
    }

    if (isClosed && !isAdmin && !isLoggedIn){
        return (
            <Redirect 
                to={{
                    pathname: '/login', 
                    state: {prevPath: rest.location.pathname}
                }}
            />
        );
    }


    return <Route {...rest} component={Component} />;
}

MyRoute.defaultProps = {
    isClosed: false,
    onlyAdmin: false,
}

MyRoute.propTypes = {
    component: PropTypes.oneOfType([PropTypes.element,PropTypes.func]).isRequired,
    onlyAdmin: PropTypes.bool,
    isClosed: PropTypes.bool,
}