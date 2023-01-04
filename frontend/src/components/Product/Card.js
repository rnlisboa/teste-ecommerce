import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "../../services/axios";
import { CardContainer, CardImage, CardTitle, CardInfo, CardQuantity, CardPrice, CardButton } from './style'
export default function Card() {

    const [products, setProducts] = useState([])
    useEffect(() => {
        async function getData() {
            const response = await axios.get('/api/products/show_all/')

            setProducts(response.data)
        }

        getData()
    }, [])

    return (
        <>
            {
                products.map(
                    product => (
                        <CardContainer key={product.id}>
                            <CardImage src={`http://127.0.0.1:8000${product.product_image}`} alt={product.product_description} />
                            <CardTitle>{product.product_description}</CardTitle>
                            <CardInfo>
                                <CardQuantity>Estoque: {product.product_quantity}</CardQuantity>
                                <CardPrice> R$ {product.product_price}</CardPrice>
                            </CardInfo>
                            <Link to={`/produto/detalhes/${product.id}`}>
                                <CardButton  >Detalhes</CardButton>
                            </Link>
                        </CardContainer>
                    ))
            }
        </>
    )
}