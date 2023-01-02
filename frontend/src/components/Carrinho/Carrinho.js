import React, { useEffect, useState } from "react";
import axios from "../../services/axios";
import {CardContainer, CardImage,CardTitle, CardInfo, CardQuantity, CardPrice, CardButton } from './style'
import { useSelector } from 'react-redux';
function Carrinho() {
  const user = useSelector(state => state.auth.user);
  const [products, setProducts] = useState([])

  useEffect(()=>{
    async function getData(){
      const resp = await axios.get(`/api/shopping/my_cart/?user=${user}`)
      console.log(resp.data)
      setProducts(resp.data)
    }

    getData()
  }, [])
  
  return (
    <>
    <h1>
        Seu carrinho
    </h1>
    {products.map(product => (
                <CardContainer key={product.id}>
                <CardImage src={'http://127.0.0.1:8000' + product.product_image} alt="Titulo da imagem" />
                <CardTitle>{product.product_description}</CardTitle>
                <CardInfo>
                    <CardQuantity>Estoque: {product.product_quantity}</CardQuantity>
                    <CardPrice> R$ {product.product_price}</CardPrice>
                </CardInfo>
              
            </CardContainer>
            ))}</>
    
  );
}

export default Carrinho;