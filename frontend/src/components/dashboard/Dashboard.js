import React, { useRef, useState } from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import axios from "../../services/axios";
import { toast } from "react-toastify";

function Dashboard() {
    const [product_image, setImage] = useState('')
    const [product_description, SetProductDescription] = useState('')
    const [product_price, SetProductPrice] = useState('')
    const [product_quantity, SetProductQuantity] = useState('')
    const imgRef = useRef()
    
    function handleImg(e){
        
        if(e.target.files[0]){
            imgRef.current.src = URL.createObjectURL(e.target.files[0])
            const foto = e.target.files[0]
            setImage(foto)
            imgRef.current.style.display = 'block'
        } else{
            imgRef.current.src = '';
            imgRef.current.style.display = 'none'
        }

    }
    async function handleRegisterProduct(e){
        e.preventDefault()

        const dados = new FormData();
        dados.append("product_description", product_description)
        dados.append("product_price", product_price)
        dados.append("product_quantity", product_quantity)
        dados.append("product_image", product_image)

        try{
            await axios.post('/api/products/register/', dados, {
                headers: {
                    "Content-type": "multipart/form-data"
                }
            })

            toast.success("Novo produto adicionado.")
        } catch(err){
            console.log(e)
        }
        // //
        // // 
        // // console.log(image)
        
       
        
        
        
        // //const formData = new FormData(e)
        // // formData.append('image', image)
        // // formData.append('descricao', product_description)
        // // formData.append('preco', product_price)
        // // formData.append('quantidade', product_quantity)
        
        // //console.log(formData)
        // const imagemURL = URL.createObjectURL(e.target.files[0])
        // setImage(imagemURL)

        // try{
        //     // const resp = await axios.post('/api/products/register/', formData, {
        //     //     headers: {
        //     //         'Content-type': 'multipart/form-data'
        //     //         ,Accept: 'application/json',
        //     //     }
        //     // })
        //     const resp = await axios.post('/api/products/register/', {
        //         product_description, product_price, product_quantity, product_image
        //     })
        //     console.log(resp.data)
        //     toast.success(resp.data)
        // } catch(e){
        //     console.log(e.response.data)
 
        //     toast.error(e.response.data)
        // }
        
    }

    
    
    return (
        <Container className="mt-5">
            <Row >
                
                <Col className="col-lg">

                    <h1>Cadastrar novo produto </h1>
                    <Form onSubmit={handleRegisterProduct}>
                        <Form.Group className="mb-3">
                            <Form.Label htmlFor="inputImage">Foto</Form.Label>
                            <Form.Control 
                            id="inputImage"
                            type="file" 
                            onChange={handleImg}
                            name="product_image"
                            />
                        </Form.Group>
                        <img style={{width:400}} alt="preview" ref={imgRef}/>

                        <Form.Group className="mb-3">
                            <Form.Label>Descrição do produto</Form.Label>
                            <Form.Control 
                            type="text" 
                            value={product_description} onChange={e => SetProductDescription(e.target.value)}
                            name="product_description"/>
                        </Form.Group>

                        <Form.Group className="mb-3">
                            <Form.Label>Preço unitário</Form.Label>
                            <Form.Control 
                            type="number" 
                            value={product_price} onChange={e => SetProductPrice(e.target.value)}
                            name="product_price" />
                        </Form.Group>

                        <Form.Group className="mb-3">
                            <Form.Label>Quantidade</Form.Label>
                            <Form.Control 
                            type="number" 
                            value={product_quantity} onChange={e => SetProductQuantity(e.target.value)}
                            name="product_quantity"/>
                        </Form.Group>

                        <Button variant="primary" type="submit">
                            Adicionar
                        </Button>
                    </Form>
                </Col>
            </Row>
        </Container>
    );
}

export default Dashboard;