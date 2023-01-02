import React, {useEffect, useState} from "react";
import { Link } from "react-router-dom";
import axios from "../../services/axios";
import { useDispatch, useSelector } from 'react-redux';
import {CardContainer, CardImage,CardTitle, CardInfo, CardQuantity, CardPrice, CardButton } from './style'
import { FaUserCircle, FaEdit, FaWindowClose, FaExclamation } from 'react-icons/fa';
import { toast } from "react-toastify";
export default function Card(){
    
    const [products, setProducts ] = useState([])
    const [idproduct, setIdproduct] = useState('')
    const isAdmin = useSelector(state => state.auth.isAdmin)
    const isLoggedIn = useSelector(state => state.auth.isLoggedIn);
    useEffect(()=>{
        async function getData(){
            const response = await axios.get('/api/products/show_all/')
            
            setProducts(response.data)
        }

        getData()
    }, [])
    
    return (
        <>
            {products.map(product => (
                <CardContainer key={product.id}>
                <CardImage src={'http://127.0.0.1:8000' + product.product_image} alt="Titulo da imagem" />
                <CardTitle>{product.product_description}</CardTitle>
                <CardInfo>
                    <CardQuantity>Estoque: {product.product_quantity}</CardQuantity>
                    <CardPrice> R$ {product.product_price}</CardPrice>
                </CardInfo>
                {
                        isAdmin ? (
                            <Link to={`/produto/detalhes/${product.id}`}>
                                <CardButton contextMenu="">Detalhes</CardButton>
                            </Link>
                            
                        
                        
                        ) : (
                            <Link to={`/produto/detalhes/${product.id}`}>
                                <CardButton type="submit" contextMenu="">Detalhes</CardButton>
                            </Link>
                            
                        )
                    }
                
                
                
                
                
                
            </CardContainer>
            ))}
            
        
        </>
        
    )
}