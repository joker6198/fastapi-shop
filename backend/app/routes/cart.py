from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.cart_service import CartService
from ..schemas.cart import CartItem, CartItemCreate, CartItemUpdate, AddToCartRequest, CartResponse, UpdateCartRequest, RemoveFromCartRequest
from pydantic import BaseModel

router = APIRouter(
    prefix='api/cart',
    tags=['cart']
)


@router.post('/add', status_code=status.HTTP_200_OK)
def add_to_cart(request: AddToCartRequest, db: Session = Depends(get_db)):
    service = CartService(db)
    item = CartItemCreate(product_id=request.product_id,
                          quantity=request.quantity)
    update_cart = service.add_to_cart(request.cart, item)
    return {'cart': update_cart}


@router.post('', response_model=CartResponse, status_code=status.HTTP_200_OK)
def get_card(cart_data: dict[int, int], db: Session = Depends(get_db)):
    service = CartService(db)
    return service.get_cart_details(cart_data)


@router.put('/update', status_code=status.HTTP_200_OK)
def update_cart_item(request: UpdateCartRequest, db: Session = Depends(get_db)):
    service = CartService(db)
    item = CartItemUpdate(product_id=request.product_id,
                          quantity=request.quantity)
    update_cart = service.update_cart_item(request.catr, item)
    return {'cart': update_cart}


@router.delete('/remove/{product_id}', status_code=status.HTTP_200_OK)
def remove_from_cart(product_id: int, request: RemoveFromCartRequest, db: Session = Depends(get_db)):
    service = CartService(db)
    update_cart = service.remove_cart_item(request.cart, product_id)
    return {'cart': update_cart}
