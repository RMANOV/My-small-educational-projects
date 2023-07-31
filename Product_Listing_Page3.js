// Product Listing Page
// Summary
// Create a Product Listing Page, resembling a typical page in an ecommerce store. The product listing
// page (PLP) is a page that contains a list of products. This page comes up after clicking on a category
// and respectively the products assigned to that category are displayed. The idea here is to make the
// customers see a list of products with the important details, thumbnail, and pricing so that the
// customer can compare and make an informed decision.
// The focus is on the front-end aspect, it is not necessary to host the application on a server. For
// sample data, you can use a data structure of your choice (e.g., JSON).
// Requirement
// General requirements:
// 1. The focus is on the front-end aspect, it is not necessary to host the application on a server.
// For sample data, you can use a data structure of your choice (e.g., JSON). You can define the
// sample data with products/data you like.
// 2. Sample data should be defined in a way that all the features below are demonstrable.
// 3. There are no requirements on what core web technologies should be used. You are free to
// use any JavaScript library/framework e.g., React.js. Bootstrap can also be used, if desired.
// The only requirement is not to use an HTML template, or ecommerce module / framework /
// platform. The intention of the task is to demonstrate proficiency in JavaScript, HTML and
// CSS.
// 4. Page should be responsive and should work well on both desktop and mobile.
// 5. Code should be committed in GitHub and link to be shared afterwards.
// 6. In addition to the code, a written summary should also be provided which explains what
// has been implemented as part of the task, with which technologies and how it was
// achieved. Also, you can include a short summary of what were the challenges.
// The following sections and functionalities should be supported by the page:
// 1. Header with simple navigational menu.
// a. To contain Logo
// b. Navigational Menu - It’s ok to have just a couple of categories. Clicking on a category
// should load different set of products depending on the category selected. (i.e., Bags
// category should open a PLP page with bags items, Shoes category should open a PLP
// page with shoes items). When a customer opens the page, the first category should
// be loaded by default.
// c. The header should be ‘sticky’ i.e., whenever customer scrolls down to the page the
// header should remain visible.2. Product counter – small section showing how many products are currently displayed in the
// product grid. (x out of y)
// 3. Product Grid
// a. Contains a set of product tiles positioned in a grid-like structure.
// b. The number of products on each row can be decided by the developer. The grid
// should not have more than 5 rows on initial loading. The Load More (see below)
// button will serve the purpose of loading more product tiles in case there are more
// than 5 rows of products.
// c. Product tile - each product tile should contain:
// i. Image of the product
// ii. Name of the product
// iii. Short description
// iv. Price (some products should have discounted price)
// v. Ratings ‘stars’.
// vi. Add to cart button – a success alert to be displayed on click (e.g., ‘Product
// added to cart’)
// 4. Filtering mechanism
// a. Capability to filter based on 2 characteristics. For example: color and price.
// b. To be positioned on the ‘left’ of the grid.
// c. You’re free to decide what should be the actual component for that: whether
// checkboxes, or slider, or colored thumbnails, etc.
// 5. Sorting mechanism
// a. Sorting dropdown above the product grid.
// b. To have multiple option for sorting the product grid:
// i. Alphabetical a-z
// ii. Alphabetical z-a
// iii. Price ascending.
// iv. Price descending.
// 6. Product Name and Description
// a. Section describing the category name and short description of it.
// b. The name should be with bigger heading.
// 7. Load More
// a. A load more button which on click will load one more ‘page’ of product tiles in the
// product grid.
// b. For example: if the product grid is 5 rows by 4 products (20). When a customer clicks
// ‘load more’ 20 more product tiles will be loaded after the initial product tiles.
// c. The load more should be ‘active’ until all potential products in the page are
// displayed.
// 8. Footer
// a. Static section containing set of links e.g., T&C, Privacy Policy, Contact Us
// See suggested page structures for desktop and mobile on the next pages. It is not
// mandatory to follow these wireframes exactly. The intention is to serve as a guiding point.

import React, { Component } from "react";
import "./Product_Listing_Page3.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faShoppingCart } from "@fortawesome/free-solid-svg-icons";
import { faStar } from "@fortawesome/free-solid-svg-icons";

class Product_Listing_Page3 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [/*...*/], //your data
            cart: [],
            cartBounce: false,
            category: "All",
            filteredData: [],
            sort: "",
        };
        this.handleCategoryChange = this.handleCategoryChange.bind(this);
        this.handleAddToCart = this.handleAddToCart.bind(this);
    }

    componentDidMount() {
        this.setState({
            filteredData: this.state.data
        });
    }

    handleAddToCart = (item) => {
        /* your implementation */
    }

    handleCategoryChange(event) {
        const category = event.target.value;
        let filteredData = [];
        if (category === "All") {
            filteredData = this.state.data;
        } else {
            filteredData = this.state.data.filter(item => item.category === category);
        }
        this.setState({ filteredData, category });
    }

    render() {
        return (
            <div>
                <Header category={this.state.category} onCategoryChange={this.handleCategoryChange} />
                {/* Add your product counter here */}
                <div>
                    {/* Sorting and filtering components */}
                </div>
                {this.state.filteredData.map(product => <Product key={product.id} product={product} handleAddToCart={this.handleAddToCart} />)}
                <Footer />
            </div>
        );
    }
}

class Header extends Component {
    render() {
        return (
            <div>
                <div>
                    {/* Logo */}
                </div>
                <div>
                    {/* Navigation menu */}
                </div>
            </div>
        );
    }
}

class Product extends Component {
    render() {
        return (
            <div>
                <div>
                    {/* Image */}
                </div>
                <div>
                    {/* Name */}
                </div>
                <div>
                    {/* Description */}
                </div>
                <div>
                    {/* Price */}
                </div>
                <div>
                    {/* Rating */}
                </div>
                <div>
                    {/* Add to cart button */}
                </div>
            </div>
        );
    }
}

class Footer extends Component {
    render() {
        return (
            <div>
                {/* Footer links */}
            </div>
        );
    }
}

export default Product_Listing_Page3;



