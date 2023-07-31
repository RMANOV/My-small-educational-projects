import React, { Component } from 'react';
import './App.css';
import './Responsive.css';


// Placeholder product data
const products = [
    // Your product data here...
];

// Define Product component
const Product = ({ product }) => (
    <div>
        <img src={product.image} alt={product.name} />
        <h2>{product.name}</h2>
        <p>{product.description}</p>
        <p>{product.price}</p>
        <p>{product.rating}</p>
        <button onClick={() => alert('Product added to cart')}>Add to Cart</button>
    </div>
);

// Define Header component
const Header = ({ category, onCategoryChange }) => {
    // Just a placeholder. Add your categories
    const categories = ["Bags", "Shoes"];

    return (
        <header>
            {/* Logo here */}
            <nav>
                {categories.map(cat => (
                    <button key={cat} onClick={() => onCategoryChange(cat)}>{cat}</button>
                ))}
            </nav>
        </header>
    );
};

// Define Footer component
const Footer = () => (
    <footer>
        {/* Add your footer links here */}
        <a href="/terms">Terms & Conditions</a>
        <a href="/privacy">Privacy Policy</a>
        <a href="/contact">Contact Us</a>
    </footer>
);

// Define App component
class App extends Component {
    state = {
        products: products.slice(0, 20), // Initially display the first 20 products
        displayedProducts: [],
        sort: 'none',
        colorFilter: '',
        priceFilter: '',
        category: '',
    };

    componentDidMount() {
        this.updateDisplayedProducts();
    }

    updateDisplayedProducts = () => {
        let displayedProducts = [...this.state.products];

        // Filtering logic
        if (this.state.colorFilter) {
            displayedProducts = displayedProducts.filter(product => product.color === this.state.colorFilter);
        }

        if (this.state.priceFilter) {
            displayedProducts = displayedProducts.filter(product => product.price <= this.state.priceFilter);
        }

        // Sorting logic
        // Add your sorting logic here
        if (this.state.sort === 'priceAsc') {
            displayedProducts = displayedProducts.sort((a, b) => a.price - b.price);
        } else if (this.state.sort === 'priceDesc') {
            displayedProducts = displayedProducts.sort((a, b) => b.price - a.price);
        } else if (this.state.sort === 'ratingAsc') {
            displayedProducts = displayedProducts.sort((a, b) => a.rating - b.rating);
        } else if (this.state.sort === 'ratingDesc') {
            displayedProducts = displayedProducts.sort((a, b) => b.rating - a.rating);
        }

        this.setState({ displayedProducts });
    };

    // Other methods ...
    productCounter = () => {
        let productCount = this.state.products.length;
        return (productCount);
    }

    loadMore = () => {
        // Load 20 more products
        const productsToAdd = products.slice(this.state.products.length, this.state.products.length + 20);
        this.setState({ products: [...this.state.products, ...productsToAdd] }, this.updateDisplayedProducts);
    };

    discountedPrice = (Price) => {
        let discount = 0.2;
        let discountedPrice = this.state.products.price * discount;
        return (discountedPrice);
    }

    handleCategoryChange = (category) => {
        // Update the products based on the category
        // Just a placeholder. You will need to actually filter products based on the category
        const newProducts = products.filter(product => product.category === category);
        this.setState({ category, products: newProducts }, this.updateDisplayedProducts);
    };

    Cart = () => {
        let cart = [];
        if (this.state.products) {
            cart = this.state.products.map(product => product.name);
        }
        Addproduct = (product) => {
            cart.push(product);
        }
        RemoveProduct = (product) => {
            cart.pop(product);
        }
        CartViewProduct = () => {
            cart.map(product => product.name);
        }

        return (cart);

    }

    render() {
        return (
            <div>
                <Header category={this.state.category} onCategoryChange={this.handleCategoryChange} />
                {/* Add your product counter here */}
                <div>
                    {/* Sorting and filtering components */}
                </div>
                {this.state.displayedProducts.map(product => <Product key={product.id} product={product} />)}
                <button onClick={this.loadMore}>Load More</button>
                <Footer />
            </div>
        );
    }
}

export default App;



// App.css

* {
    box-sizing: border-box;
}

body {
    margin: 0;

    font-family: Arial, Helvetica, sans-serif;

    background-color: #f5f5f5;

    color: #333;

    line-height: 1.5;

    font-size: 16px;

    text-align: center;

    padding: 0 20px;

    max-width: 1000px;

    margin: 0 auto;

    display: flex;

    flex-direction: column;

    min-height: 100vh;

    justify-content: space-between;

    position: relative;

    overflow-x: hidden;

    overflow-y: scroll;

    -webkit-overflow-scrolling: touch;

    -webkit-font-smoothing: antialiased;

    -moz-osx-font-smoothing: grayscale;

    text-rendering: optimizeLegibility;

    -webkit-tap-highlight-color: transparent;

    -webkit-touch-callout: none;

    -webkit-user-select: none;

    -moz-user-select: none;

    -ms-user-select: none;

    user-select: none;

}

header {
    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 20px 0;

    border-bottom: 1px solid #ccc;

}


header nav {
    display: flex;

    justify-content: center;

    align-items: center;

    flex-wrap: wrap;

    margin: 0 20px;

}

header nav button {
    border: none;

    background: none;

    font-size: 16px;

    padding: 10px 20px;

}

header nav button:hover {

    cursor: pointer;

    background-color: #eee;

}

header nav button:focus {
    
    outline: none;

}

header nav button:active {

    background-color: #ddd;

}

// responsive header

@media screen and (max-width: 600px) {

    header nav {

        margin: 0;

    }

}
