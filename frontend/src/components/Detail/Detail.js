import React, {useEffect, useState} from "react";
import { Link } from "react-router-dom";
import axios from "../../services/axios";
import { useSelector } from 'react-redux';
import {CardContainer, CardImage,CardTitle, CardInfo, CardQuantity, CardPrice, CardButton } from './style'

import { toast } from "react-toastify";
export default function Detail(props){
    const user = useSelector(state => state.auth.user);
    
    const [product, setProduct ] = useState([])
    const isAdmin = useSelector(state => state.auth.isAdmin)
    
    useEffect(()=>{
        async function getData(){
            const id = props.match.params.id
            const response = await axios.get(`/api/products/show_one/?value=${id}`)
            
            setProduct(response.data)
        }

        getData()
    }, [])
    async function handleClick(){
        const id = props.match.params.id
        try{
            await axios.post(`/api/shopping/add_to_cart/?value=${id}`,{
                user,product
            })
            toast.success('Produto salvo no carrinho.')
        } catch(e){
            toast.error('Erro ao adicionar produto ao carrinho.')
        }
        
        
    }
    return (
        <>
             {
                <CardContainer key={product.id}>
                <CardImage src={'http://127.0.0.1:8000' + product.product_image} alt="Titulo da imagem" />
                <CardTitle>{product.product_description}</CardTitle>
                <CardInfo>
                    <CardQuantity>Estoque: {product.product_quantity}</CardQuantity>
                    <CardPrice> R$ {product.product_price}</CardPrice>
                </CardInfo>
                <CardButton onClick={handleClick}>Adicionar ao carrinho</CardButton>
                
                
            </CardContainer>
            }
            
        
        </>
        
    )
}