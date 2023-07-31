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
import { faShoppingCart, faStar } from "@fortawesome/free-solid-svg-icons";

class Product_Listing_Page3 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [], //your data
            cart: [],
            cartBounce: false,
            category: "All",
            filteredData: [],
            sort: "",
            page: 1,
            productsPerPage: 20,
        };
        this.handleCategoryChange = this.handleCategoryChange.bind(this);
        this.handleAddToCart = this.handleAddToCart.bind(this);
        this.handleLoadMore = this.handleLoadMore.bind(this);
        this.handleFilterChange = this.handleFilterChange.bind(this);
    }

    componentDidMount() {
        // Fetch data from server and set state
        fetch("/api/products")
            .then((response) => response.json())
            .then((data) => {
                this.setState({
                    data: data,
                    filteredData: data.slice(0, this.state.productsPerPage),
                });
            });
    }

    handleAddToCart(item) {
        // Add item to cart
        const cart = [...this.state.cart];
        cart.push(item);
        this.setState({ cart, cartBounce: true });
        setTimeout(() => this.setState({ cartBounce: false }), 1000);
    }

    handleCategoryChange(event) {
        // Filter data by category
        const category = event.target.value;
        import React, { Component } from "react";
        import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
        import { faStar, faShoppingCart } from "@fortawesome/free-solid-svg-icons";

        class Product_Listing_Page3 extends Component {
            constructor(props) {
                super(props);
                this.state = {
                    data: [
                        {
                            id: 1,
                            name: "Product 1",
                            description: "This is a product description.",
                            price: "$10",
                            rating: 4,
                            category: "Bags",
                            color: "red",
                        },
                        {
                            id: 2,
                            name: "Product 2",
                            description: "This is a product description.",
                            price: "$20",
                            rating: 3,
                            category: "Shoes",
                            color: "green",
                        },
                        {
                            id: 3,
                            name: "Product 3",
                            description: "This is a product description.",
                            price: "$30",
                            rating: 5,
                            category: "Bags",
                            color: "blue",
                        },
                        {
                            id: 4,
                            name: "Product 4",
                            description: "This is a product description.",
                            price: "$40",
                            rating: 2,
                            category: "Shoes",
                            color: "red",
                        },
                        {
                            id: 5,
                            name: "Product 5",
                            description: "This is a product description.",
                            price: "$50",
                            rating: 4,
                            category: "Bags",
                            color: "green",
                        },
                        {
                            id: 6,
                            name: "Product 6",
                            description: "This is a product description.",
                            price: "$60",
                            rating: 3,
                            category: "Shoes",
                            color: "blue",
                        },
                        {
                            id: 7,
                            name: "Product 7",
                            description: "This is a product description.",
                            price: "$70",
                            rating: 5,
                            category: "Bags",
                            color: "red",
                        },
                        {
                            id: 8,
                            name: "Product 8",
                            description: "This is a product description.",
                            price: "$80",
                            rating: 2,
                            category: "Shoes",
                            color: "green",
                        },
                        {
                            id: 9,
                            name: "Product 9",
                            description: "This is a product description.",
                            price: "$90",
                            rating: 4,
                            category: "Bags",
                            color: "blue",
                        },
                        {
                            id: 10,
                            name: "Product 10",
                            description: "This is a product description.",
                            price: "$100",
                            rating: 3,
                            category: "Shoes",
                            color: "red",
                        },
                    ],
                    filteredData: [],
                    category: "All",
                    sort: "",
                    page: 1,
                    productsPerPage: 6,
                };
                this.handleCategoryChange = this.handleCategoryChange.bind(this);
                this.handleAddToCart = this.handleAddToCart.bind(this);
                this.handleLoadMore = this.handleLoadMore.bind(this);
                this.handleFilterChange = this.handleFilterChange.bind(this);
            }

            componentDidMount() {
                // Load initial data
                const filteredData = this.state.data.slice(0, this.state.productsPerPage);
                this.setState({ filteredData });
            }

            handleCategoryChange(event) {
                // Filter data by category
                const category = event.target.value;
                let filteredData = [];
                if (category === "All") {
                    filteredData = this.state.data.slice(0, this.state.productsPerPage);
                } else {
                    filteredData = this.state.data
                        .filter((item) => item.category === category)
                        .slice(0, this.state.productsPerPage);
                }
                this.setState({ filteredData, category, page: 1 });
            }

            handleAddToCart(product) {
                // Add product to cart
                console.log(`Added ${product.name} to cart.`);
            }

            handleLoadMore() {
                // Load more products
                const nextPage = this.state.page + 1;
                const startIndex = (nextPage - 1) * this.state.productsPerPage;
                const endIndex = nextPage * this.state.productsPerPage;
                const newData = this.state.data.slice(startIndex, endIndex);
                const filteredData = [...this.state.filteredData, ...newData];
                this.setState({ filteredData, page: nextPage });
            }

            handleFilterChange(event) {
                // Filter data by color
                const color = event.target.value;
                let filteredData = [];
                class Product_Listing_Page3 extends Component {
                    constructor(props) {
                        super(props);
                        this.state = {
                            data: [], // array of all products
                            filteredData: [], // array of filtered products
                            category: "All", // selected category
                            sort: "", // selected sorting option
                            color: "", // selected color filter
                            page: 1, // current page number
                            productsPerPage: 6, // number of products to show per page
                        };
                        this.handleCategoryChange = this.handleCategoryChange.bind(this);
                        this.handleFilterChange = this.handleFilterChange.bind(this);
                        this.handleLoadMore = this.handleLoadMore.bind(this);
                        this.handleAddToCart = this.handleAddToCart.bind(this);
                        this.handleSortChange = this.handleSortChange.bind(this);
                    }

                    componentDidMount() {
                        // fetch data and set state
                        const data = [
                            {
                                id: 1,
                                name: "Product 1",
                                description: "This is a description of product 1",
                                price: 10,
                                rating: 3,
                                category: "Bags",
                                color: "red",
                            },
                            {
                                id: 2,
                                name: "Product 2",
                                description: "This is a description of product 2",
                                price: 20,
                                rating: 4,
                                category: "Shoes",
                                color: "green",
                            },
                            {
                                id: 3,
                                name: "Product 3",
                                description: "This is a description of product 3",
                                price: 30,
                                rating: 5,
                                category: "Bags",
                                color: "blue",
                            },
                            {
                                id: 4,
                                name: "Product 4",
                                description: "This is a description of product 4",
                                price: 40,
                                rating: 2,
                                category: "Shoes",
                                color: "red",
                            },
                            {
                                id: 5,
                                name: "Product 5",
                                description: "This is a description of product 5",
                                price: 50,
                                rating: 1,
                                category: "Bags",
                                color: "green",
                            },
                            {
                                id: 6,
                                name: "Product 6",
                                description: "This is a description of product 6",
                                price: 60,
                                rating: 4,
                                category: "Shoes",
                                color: "blue",
                            },
                            {
                                id: 7,
                                name: "Product 7",
                                description: "This is a description of product 7",
                                price: 70,
                                rating: 3,
                                category: "Bags",
                                color: "red",
                            },
                            {
                                id: 8,
                                name: "Product 8",
                                description: "This is a description of product 8",
                                price: 80,
                                rating: 5,
                                category: "Shoes",
                                color: "green",
                            },
                            {
                                id: 9,
                                name: "Product 9",
                                description: "This is a description of product 9",
                                price: 90,
                                rating: 2,
                                category: "Bags",
                                color: "blue",
                            },
                            {
                                id: 10,
                                name: "Product 10",
                                description: "This is a description of product 10",
                                price: 100,
                                rating: 1,
                                category: "Shoes",
                                color: "red",
                            },
                            {
                                id: 11,
                                name: "Product 11",
                                description: "This is a description of product 11",
                                price: 110,
                                rating: 4,
                                category: "Bags",
                                color: "green",
                            },
                            {
                                id: 12,
                                name: "Product 12",
                                description: "This is a description of product 12",
                                price: 120,
                                rating: 3,
                                category: "Shoes",
                                color: "blue",
                            },
                        ];
                        this.setState({ data, filteredData: data.slice(0, this.state.productsPerPage) });
                    }

                    handleCategoryChange(event) {
                        // update category and filter data
                        const category = event.target.value;
                        let filteredData;
                        if (category === "All") {
                            filteredData = this.state.data.filter((item) => this.state.color === "" || item.color === this.state.color);
                        } else {
                            filteredData = this.state.data
                                .filter((item) => item.category === category)
                                .filter((item) => this.state.color === "" || item.color === this.state.color);
                        }
                        this.setState({ category, filteredData, page: 1 });
                    }

                    handleFilterChange(event) {
                        // update color filter and filter data
                        const color = event.target.value;
                        let filteredData;
                        if (this.state.category === "All") {
                            filteredData = this.state.data.filter((item) => color === "" || item.color === color);
                        } else {
                            filteredData = this.state.data
                                .filter((item) => item.category === this.state.category)
                                .filter((item) => color === "" || item.color === color);
                        }
                        this.setState({ color, filteredData, page: 1 });
                    }

                    handleLoadMore() {
                        import React, { Component } from 'react';
                        import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
                        import { faShoppingCart } from '@fortawesome/free-solid-svg-icons';
                        import Header from './Header';
                        import ProductList from './ProductList';

                        class App extends Component {
                            constructor(props) {
                                super(props);
                                this.state = {
                                    data: [
                                        { id: 1, name: 'Product 1', price: 100, category: 'Category 1', color: 'Red' },
                                        { id: 2, name: 'Product 2', price: 200, category: 'Category 2', color: 'Green' },
                                        { id: 3, name: 'Product 3', price: 300, category: 'Category 1', color: 'Blue' },
                                        { id: 4, name: 'Product 4', price: 400, category: 'Category 2', color: 'Red' },
                                        { id: 5, name: 'Product 5', price: 500, category: 'Category 1', color: 'Green' },
                                        { id: 6, name: 'Product 6', price: 600, category: 'Category 2', color: 'Blue' },
                                        { id: 7, name: 'Product 7', price: 700, category: 'Category 1', color: 'Red' },
                                        { id: 8, name: 'Product 8', price: 800, category: 'Category 2', color: 'Green' },
                                        { id: 9, name: 'Product 9', price: 900, category: 'Category 1', color: 'Blue' },
                                        { id: 10, name: 'Product 10', price: 1000, category: 'Category 2', color: 'Red' },
                                    ],
                                    filteredData: [],
                                    category: 'All',
                                    color: 'All',
                                    sort: 'name-asc',
                                    cart: [],
                                    page: 1,
                                    productsPerPage: 4,
                                };
                                this.handleCategoryChange = this.handleCategoryChange.bind(this);
                                this.handleFilterChange = this.handleFilterChange.bind(this);
                                this.handleSortChange = this.handleSortChange.bind(this);
                                this.handleAddToCart = this.handleAddToCart.bind(this);
                                this.handleRemoveFromCart = this.handleRemoveFromCart.bind(this);
                                this.handleClearCart = this.handleClearCart.bind(this);
                                this.handleLoadMore = this.handleLoadMore.bind(this);
                            }

                            componentDidMount() {
                                this.setState({ filteredData: this.state.data });
                            }

                            handleCategoryChange(event) {
                                const category = event.target.value;
                                const color = this.state.color;
                                let filteredData = [...this.state.data];
                                if (category !== 'All') {
                                    filteredData = filteredData.filter((product) => product.category === category);
                                }
                                if (color !== 'All') {
                                    filteredData = filteredData.filter((product) => product.color === color);
                                }
                                this.setState({ category, filteredData });
                            }

                            handleFilterChange(event) {
                                import React from 'react';
                                import Header from './Header';
                                import ProductList from './ProductList';

                                class App extends React.Component {
                                    constructor(props) {
                                        super(props);
                                        this.state = {
                                            data: [
                                                {
                                                    id: 1,
                                                    name: 'Product 1',
                                                    price: 100,
                                                    color: 'Red',
                                                    category: 'Category 1',
                                                    discount: 10,
                                                },
                                                {
                                                    id: 2,
                                                    name: 'Product 2',
                                                    price: 200,
                                                    color: 'Blue',
                                                    category: 'Category 2',
                                                    discount: 20,
                                                },
                                                {
                                                    id: 3,
                                                    name: 'Product 3',
                                                    price: 300,
                                                    color: 'Green',
                                                    category: 'Category 1',
                                                    discount: 5,
                                                },
                                                {
                                                    id: 4,
                                                    name: 'Product 4',
                                                    price: 400,
                                                    color: 'Yellow',
                                                    category: 'Category 2',
                                                    discount: 15,
                                                },
                                                {
                                                    id: 5,
                                                    name: 'Product 5',
                                                    price: 500,
                                                    color: 'Red',
                                                    category: 'Category 1',
                                                    discount: 0,
                                                },
                                                {
                                                    id: 6,
                                                    name: 'Product 6',
                                                    price: 600,
                                                    color: 'Blue',
                                                    category: 'Category 2',
                                                    discount: 25,
                                                },
                                                {
                                                    id: 7,
                                                    name: 'Product 7',
                                                    price: 700,
                                                    color: 'Green',
                                                    category: 'Category 1',
                                                    discount: 10,
                                                },
                                                {
                                                    id: 8,
                                                    name: 'Product 8',
                                                    price: 800,
                                                    color: 'Yellow',
                                                    category: 'Category 2',
                                                    discount: 20,
                                                },
                                            ],
                                            filteredData: [],
                                            category: 'All',
                                            color: 'All',
                                            sort: 'name-asc',
                                            cart: [],
                                            page: 1,
                                            productsPerPage: 4,
                                        };
                                        this.handleCategoryChange = this.handleCategoryChange.bind(this);
                                        this.handleFilterChange = this.handleFilterChange.bind(this);
                                        this.handleLoadMore = this.handleLoadMore.bind(this);
                                        this.handleAddToCart = this.handleAddToCart.bind(this);
                                        this.handleRemoveFromCart = this.handleRemoveFromCart.bind(this);
                                        this.handleClearCart = this.handleClearCart.bind(this);
                                        this.handleSortChange = this.handleSortChange.bind(this);
                                    }

                                    componentDidMount() {
                                        this.setState({ filteredData: this.state.data });
                                    }

                                    handleCategoryChange(event) {
                                        const category = event.target.value;
                                        const color = this.state.color;
                                        let filteredData = [...this.state.data];
                                        if (category !== 'All') {
                                            filteredData = filteredData.filter((product) => product.category === category);
                                        }
                                        if (color !== 'All') {
                                            filteredData = filteredData.filter((product) => product.color === color);
                                        }
                                        this.setState({ category, filteredData });
                                    }

                                    handleFilterChange(event) {
                                        const color = event.target.value;
                                        const category = this.state.category;
                                        let filteredData = [...this.state.data];
                                        if (color !== 'All') {
                                            filteredData = filteredData.filter((product) => product.color === color);
                                        }
                                        if (category !== 'All') {
                                            filteredData = filteredData.filter((product) => product.category === category);
                                        }
                                        this.setState({ color, filteredData });
                                    }

                                    handleLoadMore() {
                                        const page = this.state.page + 1;
                                        import React, { Component } from 'react';
                                        import Header from './Header';
                                        import ProductList from './ProductList';

                                        class App extends Component {
                                            state = {
                                                data: [],
                                                filteredData: [],
                                                cart: [],
                                                category: 'all',
                                                sort: 'name-asc',
                                                page: 1,
                                                productsPerPage: 8,
                                            };

                                            componentDidMount() {
                                                fetch('https://fakestoreapi.com/products')
                                                    .then((res) => res.json())
                                                    .then((data) => this.setState({ data, filteredData: data }));
                                            }

                                            handleCategoryChange = (category) => {
                                                this.setState({ category, page: 1 }, this.filterData);
                                            };

                                            handleFilterChange = (filter) => {
                                                this.setState({ filter, page: 1 }, this.filterData);
                                            };

                                            filterData = () => {
                                                const { data, category, filter } = this.state;
                                                let filteredData = data.filter((product) => {
                                                    if (category === 'all') {
                                                        return true;
                                                    } else {
                                                        return product.category === category;
                                                    }
                                                });
                                                if (filter) {
                                                    filteredData = filteredData.filter((product) => product.price <= filter);
                                                }
                                                this.setState({ filteredData });
                                            };

                                            handleLoadMore = () => {
                                                const { page, productsPerPage } = this.state;
                                                const startIndex = (page - 1) * productsPerPage;
                                                const endIndex = startIndex + productsPerPage;
                                                const filteredData = [...this.state.filteredData, ...this.state.data.slice(startIndex, endIndex)];
                                                this.setState({ filteredData, page: page + 1 });
                                            };

                                            handleAddToCart = (product) => {
                                                this.setState((prevState) => ({
                                                    import React, { Component } from 'react';
                                                    import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
                                                    import { faShoppingCart } from '@fortawesome/free-solid-svg-icons';
                                                    import Header from './Header';
                                                    import ProductList from './ProductList';

                                                    class App extends Component {
                                                        state = {
                                                            data: [],
                                                            filteredData: [],
                                                            category: 'all',
                                                            filter: '',
                                                            cart: [],
                                                            sort: 'name-asc',
                                                            page: 1,
                                                            productsPerPage: 6,
                                                        };

                                                        componentDidMount() {
                                                            fetch('https://fakestoreapi.com/products')
                                                                .then((res) => res.json())
                                                                .then((data) => {
                                                                    this.setState({ data, filteredData: data });
                                                                })
                                                                .catch((err) => console.log(err));
                                                        }

                                                        handleCategoryChange = (category) => {
                                                            this.setState({ category }, this.filterData);
                                                        };

                                                        handleFilterChange = (filter) => {
                                                            this.setState({ filter }, this.filterData);
                                                        };

                                                        filterData = () => {
                                                            const { data, category, filter } = this.state;
                                                            let filteredData = data.filter((product) => {
                                                                if (category === 'all' || product.category === category) {
                                                                    return product.title.toLowerCase().includes(filter.toLowerCase());
                                                                }
                                                                return false;
                                                            });
                                                            this.setState({ filteredData });
                                                        };

                                                        handleLoadMore = () => {
                                                            this.setState((prevState) => ({ page: prevState.page + 1 }));
                                                        };

                                                        handleAddToCart = (product) => {
                                                            this.setState((prevState) => ({
                                                                cart: [...prevState.cart, product],
                                                            }));
                                                            window.alert('Product added to cart');
                                                        };

                                                        handleRemoveFromCart = (product) => {
                                                            this.setState((prevState) => ({
                                                                cart: prevState.cart.filter((item) => item.id !== product.id),
                                                            }));
                                                        };

                                                        handleClearCart = () => {
                                                            this.setState({ cart: [] });
                                                        class App extends React.Component {
                                                            state = {
                                                                data: [],
                                                                filteredData: [],
                                                                category: '',
                                                                filter: '',
                                                                cart: [],
                                                                sort: 'name-asc',
                                                                page: 1,
                                                                productsPerPage: 6,
                                                            };

                                                            async componentDidMount() {
                                                                const response = await fetch('https://fakestoreapi.com/products');
                                                                const data = await response.json();
                                                                this.setState({ data, filteredData: data });
                                                            }

                                                            handleCategoryChange = (event) => {
                                                                const category = event.target.value;
                                                                const filteredData = this.state.data.filter((product) => product.category === category);
                                                                this.setState({ category, filteredData });
                                                            };

                                                            handleFilterChange = (event) => {
                                                                const filter = event.target.value;
                                                                const filteredData = this.state.data.filter((product) => product.title.toLowerCase().includes(filter.toLowerCase()));
                                                                this.setState({ filter, filteredData });
                                                            };

                                                            handleAddToCart = (product) => {
                                                                const cart = [...this.state.cart];
                                                                const index = cart.findIndex((item) => item.id === product.id);
                                                                if (index === -1) {
                                                                    cart.push({ ...product, quantity: 1 });
                                                                } else {
                                                                    cart[index].quantity++;
                                                                }
                                                                this.setState({ cart });
                                                            };

                                                            handleRemoveFromCart = (product) => {
                                                                const cart = [...this.state.cart];
                                                                const index = cart.findIndex((item) => item.id === product.id);
                                                                if (index !== -1) {
                                                                    if (cart[index].quantity === 1) {
                                                                        cart.splice(index, 1);
                                                                    } else {
                                                                        cart[index].quantity--;
                                                                    }
                                                                    this.setState({ cart });
                                                                }
                                                            };

                                                            handleLoadMore = () => {
                                                                this.setState((prevState) => ({ page: prevState.page + 1 }));
                                                            };

                                                            handleSortChange = (event) => {
                                                                import React, { Component } from 'react';
                                                                import Header from './Header';
                                                                import ProductList from './ProductList';

                                                                class App extends Component {
                                                                    state = {
                                                                        products: [],
                                                                        filteredData: [],
                                                                        cart: [],
                                                                        category: '',
                                                                        sort: '',
                                                                        page: 1,
                                                                        productsPerPage: 6,
                                                                    };

                                                                    componentDidMount() {
                                                                        fetch('https://fakestoreapi.com/products')
                                                                            .then((res) => res.json())
                                                                            .then((json) => {
                                                                                this.setState({ products: json, filteredData: json });
                                                                            });
                                                                    }

                                                                    handleCategoryChange = (event) => {
                                                                        const category = event.target.value;
                                                                        const filteredData = this.state.products.filter((product) => {
                                                                            return product.category === category || category === '';
                                                                        });
                                                                        this.setState({ category, filteredData, page: 1 });
                                                                    };

                                                                    handleFilterChange = (event) => {
                                                                        const filter = event.target.value;
                                                                        const filteredData = this.state.products.filter((product) => {
                                                                            return product.title.toLowerCase().includes(filter.toLowerCase());
                                                                        });
                                                                        this.setState({ filteredData, page: 1 });
                                                                    };

                                                                    handleSortChange = (event) => {
                                                                        const sort = event.target.value;
                                                                        let filteredData = [...this.state.filteredData];
                                                                        if (sort === 'name-asc') {
                                                                            filteredData.sort((a, b) => a.title.localeCompare(b.title));
                                                                        } else if (sort === 'name-desc') {
                                                                            filteredData.sort((a, b) => b.title.localeCompare(a.title));
                                                                        } else if (sort === 'price-asc') {
                                                                            filteredData.sort((a, b) => a.price - b.price);
                                                                        } else if (sort === 'price-desc') {
                                                                            filteredData.sort((a, b) => b.price - a.price);
                                                                        }
                                                                        this.setState({ sort, filteredData });
                                                                    };

                                                                    handleAddToCart = (product) => {
                                                                        const cart = [...this.state.cart];
                                                                        const index = cart.findIndex((item) => item.id === product.id);
                                                                        if (index === -1) {
                                                                            cart.push({ ...product, quantity: 1 });
                                                                        } else {
                                                                            cart[index].quantity++;
                                                                        }
                                                                        this.setState({ cart });
                                                                    };

                                                                    handleRemoveFromCart = (product) => {
                                                                        const cart = [...this.state.cart];
                                                                        const index = cart.findIndex((item) => item.id === product.id);
                                                                        import React, { Component } from 'react';
                                                                        import Header from './Header';
                                                                        import ProductList from './ProductList';

                                                                        class App extends Component {
                                                                            state = {
                                                                                category: '',
                                                                                filter: '',
                                                                                cart: [],
                                                                                sort: 'name-asc',
                                                                                page: 1,
                                                                                productsPerPage: 6,
                                                                                products: [],
                                                                            };

                                                                            componentDidMount() {
                                                                                // Fetch products data and set it to state
                                                                                fetch('/api/products')
                                                                                    .then((response) => response.json())
                                                                                    .then((data) => this.setState({ products: data }));
                                                                            }

                                                                            handleCategoryChange = (category) => {
                                                                                this.setState({ category, page: 1 });
                                                                            };

                                                                            handleFilterChange = (filter) => {
                                                                                this.setState({ filter, page: 1 });
                                                                            };

                                                                            handleSortChange = (event) => {
                                                                                this.setState({ sort: event.target.value });
                                                                            };

                                                                            handleAddToCart = (product) => {
                                                                                const { cart } = this.state;
                                                                                const index = cart.findIndex((item) => item.id === product.id);
                                                                                if (index !== -1) {
                                                                                    cart[index].quantity++;
                                                                                } else {
                                                                                    cart.push({ ...product, quantity: 1 });
                                                                                }
                                                                                this.setState({ cart });
                                                                            };

                                                                            handleRemoveFromCart = (product) => {
                                                                                const { cart } = this.state;
                                                                                const index = cart.findIndex((item) => item.id === product.id);
                                                                                if (index !== -1) {
                                                                                    cart[index].quantity--;
                                                                                    if (cart[index].quantity === 0) {
                                                                                        cart.splice(index, 1);
                                                                                    }
                                                                                    this.setState({ cart });
                                                                                }
                                                                            };

                                                                            handleLoadMore = () => {
                                                                                this.setState({ page: this.state.page + 1 });
                                                                            };

                                                                            render() {
                                                                                const { category, filter, cart, sort, page, productsPerPage, products } = this.state;

                                                                                // Filter and sort products
                                                                                const filteredData = products.filter((product) => {
                                                                                    if (category && product.category !== category) {
                                                                                        import React, { Component } from 'react';
                                                                                        import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
                                                                                        import { faShoppingCart } from '@fortawesome/free-solid-svg-icons';
                                                                                        import Header from './Header';
                                                                                        import ProductList from './ProductList';

                                                                                        class App extends Component {
                                                                                            state = {
                                                                                                category: '',
                                                                                                filter: '',
                                                                                                sort: 'name-asc',
                                                                                                cart: [],
                                                                                                page: 1,
                                                                                                productsPerPage: 6,
                                                                                                data: [
                                                                                                    {
                                                                                                        id: 1,
                                                                                                        name: 'Product 1',
                                                                                                        category: 'Category 1',
                                                                                                        price: 10,
                                                                                                        image: 'https://via.placeholder.com/150',
                                                                                                    },
                                                                                                    {
                                                                                                        id: 2,
                                                                                                        name: 'Product 2',
                                                                                                        category: 'Category 2',
                                                                                                        price: 20,
                                                                                                        image: 'https://via.placeholder.com/150',
                                                                                                    },
                                                                                                    {
                                                                                                        id: 3,
                                                                                                        name: 'Product 3',
                                                                                                        category: 'Category 1',
                                                                                                        price: 30,
                                                                                                        image: 'https://via.placeholder.com/150',
                                                                                                    },
                                                                                                    {
                                                                                                        id: 4,
                                                                                                        name: 'Product 4',
                                                                                                        category: 'Category 2',
                                                                                                        price: 40,
                                                                                                        image: 'https://via.placeholder.com/150',
                                                                                                    },
                                                                                                    {
                                                                                                        id: 5,
                                                                                                        name: 'Product 5',
                                                                                                        category: 'Category 1',
                                                                                                        price: 50,
                                                                                                        image: 'https://via.placeholder.com/150',
                                                                                                    },
                                                                                                    {
                                                                                                        id: 6,
                                                                                                        name: 'Product 6',
                                                                                                        category: 'Category 2',
                                                                                                        price: 60,
                                                                                                        image: 'https://via.placeholder.com/150',
                                                                                                    },
                                                                                                    {
                                                                                                        id: 7,
                                                                                                        name: 'Product 7',
                                                                                                        category: 'Category 1',
                                                                                                        price: 70,
                                                                                                        image: 'https://via.placeholder.com/150',
                                                                                                    },
                                                                                                    {
                                                                                                        id: 8,
                                                                                                        name: 'Product 8',
                                                                                                        category: 'Category 2',
                                                                                                        price: 80,
                                                                                                        image: 'https://via.placeholder.com/150',
                                                                                                    },
                                                                                                    {
                                                                                                        id: 9,
                                                                                                        name: 'Product 9',
                                                                                                        category: 'Category 1',
                                                                                                        price: 90,
                                                                                                        image: 'https://via.placeholder.com/150',
                                                                                                    },
                                                                                                    {
                                                                                                        id: 10,
                                                                                                        name: 'Product 10',
                                                                                                        category: 'Category 2',
                                                                                                        price: 100,
                                                                                                        image: 'https://via.placeholder.com/150',
                                                                                                    },
                                                                                                ],
                                                                                            };

                                                                                            handleCategoryChange = (event) => {
                                                                                                this.setState({ category: event.target.value, page: 1 });
                                                                                            };

                                                                                            handleFilterChange = (event) => {
                                                                                                this.setState({ filter: event.target.value, page: 1 });
                                                                                            };

                                                                                            handleSortChange = (event) => {
                                                                                                this.setState({ sort: event.target.value, page: 1 });
                                                                                            };

                                                                                            handleAddToCart = (product) => {
                                                                                                const { cart } = this.state;
                                                                                                const productIndex = cart.findIndex((p) => p.id === product.id);
                                                                                                if (productIndex === -1) {
                                                                                                    this.setState({ cart: [...cart, { ...product, quantity: 1 }] });
                                                                                                } else {
                                                                                                    const updatedCart = [...cart];
                                                                                                    updatedCart[productIndex].quantity += 1;
                                                                                                    this.setState({ cart: updatedCart });
                                                                                                }
                                                                                            };

                                                                                            handleRemoveFromCart = (product) => {
                                                                                                const { cart } = this.state;
                                                                                                const productIndex = cart.findIndex((p) => p.id === product.id);
                                                                                                if (productIndex !== -1) {
                                                                                                    const updatedCart = [...cart];
                                                                                                    if (updatedCart[productIndex].quantity === 1) {
                                                                                                        updatedCart.splice(productIndex, 1);
                                                                                                    } else {
                                                                                                        updatedCart[productIndex].quantity -= 1;
                                                                                                    }
                                                                                                    this.setState({ cart: updatedCart });
                                                                                                }
                                                                                            };

                                                                                            handleLoadMore = () => {
                                                                                                this.setState((prevState) => ({ page: prevState.page + 1 }));
                                                                                            };

                                                                                            render() {
                                                                                                const { category, filter, sort, cart, page, productsPerPage, data } = this.state;

                                                                                                // Filter products
                                                                                                const filteredData = data.filter((product) => {
                                                                                                    if (category && product.category !== category) {
                                                                                                        return false;
                                                                                                    }
                                                                                                    if (filter && !product.name.toLowerCase().includes(filter.toLowerCase())) {
                                                                                                        return false;
                                                                                                    }
                                                                                                    return true;
                                                                                                import React, { Component } from 'react';
                                                                                                import Header from './Header';
                                                                                                import ProductList from './ProductList';

                                                                                                class App extends Component {
                                                                                                    constructor(props) {
                                                                                                        super(props);
                                                                                                        this.state = {
                                                                                                            category: 'all',
                                                                                                            filter: '',
                                                                                                            sort: 'name-asc',
                                                                                                            page: 1,
                                                                                                            productsPerPage: 6,
                                                                                                            cart: []
                                                                                                        };
                                                                                                        this.handleCategoryChange = this.handleCategoryChange.bind(this);
                                                                                                        this.handleFilterChange = this.handleFilterChange.bind(this);
                                                                                                        this.handleSortChange = this.handleSortChange.bind(this);
                                                                                                        this.handleLoadMore = this.handleLoadMore.bind(this);
                                                                                                        this.handleAddToCart = this.handleAddToCart.bind(this);
                                                                                                        this.handleRemoveFromCart = this.handleRemoveFromCart.bind(this);
                                                                                                    }

                                                                                                    handleCategoryChange(category) {
                                                                                                        this.setState({
                                                                                                            category: category,
                                                                                                            page: 1
                                                                                                        });
                                                                                                    }

                                                                                                    handleFilterChange(filter) {
                                                                                                        this.setState({
                                                                                                            filter: filter,
                                                                                                            page: 1
                                                                                                        });
                                                                                                    }

                                                                                                    handleSortChange(event) {
                                                                                                        this.setState({
                                                                                                            sort: event.target.value,
                                                                                                            page: 1
                                                                                                        });
                                                                                                    }

                                                                                                    handleLoadMore() {
                                                                                                        this.setState({
                                                                                                            page: this.state.page + 1
                                                                                                        });
                                                                                                    }

                                                                                                    handleAddToCart(product) {
                                                                                                        const cart = [...this.state.cart];
                                                                                                        const index = cart.findIndex(item => item.id === product.id);
                                                                                                        if (index === -1) {
                                                                                                            cart.push({ ...product, quantity: 1 });
                                                                                                        } else {
                                                                                                            cart[index].quantity++;
                                                                                                        }
                                                                                                        this.setState({ cart });
                                                                                                    }

                                                                                                    handleRemoveFromCart(product) {
                                                                                                        const cart = [...this.state.cart];
                                                                                                        const index = cart.findIndex(item => item.id === product.id);
                                                                                                        if (index !== -1) {
                                                                                                            if (cart[index].quantity === 1) {
                                                                                                                cart.splice(index, 1);
                                                                                                            } else {
                                                                                                                cart[index].quantity--;
                                                                                                            }
                                                                                                            this.setState({ cart });
                                                                                                        }
                                                                                                    }

                                                                                                    render() {
                                                                                                        const { category, filter, sort, page, productsPerPage, cart } = this.state;

                                                                                                        // Filter products by category and search filter
                                                                                                        const filteredData = this.props.data.filter(product => {
                                                                                                            if (category !== 'all' && product.category !== category) {
                                                                                                                return false;
                                                                                                            }
                                                                                                            if (filter && !product.name.toLowerCase().includes(filter.toLowerCase())) {
                                                                                                                return false;
                                                                                                            }
                                                                                                            return true;
                                                                                                        });

                                                                                                        // Sort products by selected sort option
                                                                                                        const sortedData = filteredData.sort((a, b) => {
                                                                                                            import React from 'react';
                                                                                                            import Header from './Header';
                                                                                                            import ProductList from './ProductList';

                                                                                                            class App extends React.Component {
                                                                                                                constructor(props) {
                                                                                                                    super(props);
                                                                                                                    this.state = {
                                                                                                                        category: 'all',
                                                                                                                        filter: '',
                                                                                                                        sort: 'name-asc',
                                                                                                                        page: 1,
                                                                                                                        productsPerPage: 6,
                                                                                                                        cart: [],
                                                                                                                        showCart: false // added state to toggle cart visibility
                                                                                                                    };
                                                                                                                    this.handleCategoryChange = this.handleCategoryChange.bind(this);
                                                                                                                    this.handleFilterChange = this.handleFilterChange.bind(this);
                                                                                                                    this.handleSortChange = this.handleSortChange.bind(this);
                                                                                                                    this.handleLoadMore = this.handleLoadMore.bind(this);
                                                                                                                    this.handleAddToCart = this.handleAddToCart.bind(this);
                                                                                                                    this.handleRemoveFromCart = this.handleRemoveFromCart.bind(this);
                                                                                                                    this.handleCartToggle = this.handleCartToggle.bind(this); // added cart toggle handler
                                                                                                                }

                                                                                                                handleCategoryChange(category) {
                                                                                                                    this.setState({
                                                                                                                        category: category,
                                                                                                                        page: 1 // reset page when category changes
                                                                                                                    });
                                                                                                                }

                                                                                                                handleFilterChange(filter) {
                                                                                                                    this.setState({
                                                                                                                        filter: filter,
                                                                                                                        page: 1 // reset page when filter changes
                                                                                                                    });
                                                                                                                }

                                                                                                                handleSortChange(event) {
                                                                                                                    this.setState({
                                                                                                                        sort: event.target.value
                                                                                                                    });
                                                                                                                }

                                                                                                                handleLoadMore() {
                                                                                                                    this.setState({
                                                                                                                        page: this.state.page + 1
                                                                                                                    });
                                                                                                                }

                                                                                                                handleAddToCart(product) {
                                                                                                                    const cart = [...this.state.cart];
                                                                                                                    const index = cart.findIndex(item => item.id === product.id);
                                                                                                                    if (index === -1) {
                                                                                                                        cart.push({...product, quantity: 1});
                                                                                                                    } else {
                                                                                                                        cart[index].quantity++;
                                                                                                                    }
                                                                                                                    this.setState({
                                                                                                                        cart: cart
                                                                                                                    });
                                                                                                                }

                                                                                                                handleRemoveFromCart(product) {
                                                                                                                    const cart = [...this.state.cart];
                                                                                                                    const index = cart.findIndex(item => item.id === product.id);
                                                                                                                    if (index !== -1) {
                                                                                                                        if (cart[index].quantity === 1) {
                                                                                                                            cart.splice(index, 1);
                                                                                                                        } else {
                                                                                                                            cart[index].quantity--;
                                                                                                                        }
                                                                                                                        this.setState({
                                                                                                                            cart: cart
                                                                                                                        });
                                                                                                                    }
                                                                                                                }

                                                                                                                handleCartToggle() {
                                                                                                                    this.setState({
                                                                                                                        showCart: !this.state.showCart
                                                                                                                    });
                                                                                                                }

                                                                                                                render() {
                                                                                                                    const {category, filter, sort, page, productsPerPage, cart, showCart} = this.state;
                                                                                                                    const filteredData = this.props.products.filter(product => {
                                                                                                                        return (category === 'all' || product.category === category) &&
                                                                                                                            (filter === '' || product.name.toLowerCase().includes(filter.toLowerCase()));
                                                                                                                    });
                                                                                                                    const sortedData = filteredData.sort((a, b) => {
                                                                                                                        const [aKey, aOrder] = a[sort.split('-')[0]];
                                                                                                                        const [bKey, bOrder] = b[sort.split('-')[0]];
                                                                                                                        if (a[aKey] < b[bKey]) {
                                                                                                                            return aOrder === 'asc' ? -1 : 1;
                                                                                                                        }
                                                                                                                        if (a[aKey] > b[bKey]) {
                                                                                                                            return aOrder === 'asc' ? 1 : -1;
                                                                                                                        }
                                                                                                                        return 0;
                                                                                                                    });
                                                                                                                    const startIndex = (page - 1) * productsPerPage;
                                                                                                                    const endIndex = startIndex + productsPerPage;
                                                                                                                    const paginatedData = sortedData.slice(startIndex, endIndex);

                                                                                                                    return (
                                                                                                                        <div>
                                                                                                                            <Header category={category} onCategoryChange={this.handleCategoryChange} onFilterChange={this.handleFilterChange} cart={cart} onCartToggle={this.handleCartToggle} /> {/* added cart toggle handler */}
                                                                                                                            import React, { Component } from 'react';
                                                                                                                            import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
                                                                                                                            import { faShoppingCart } from '@fortawesome/free-solid-svg-icons';
                                                                                                                            import Header from './Header';
                                                                                                                            import ProductList from './ProductList';

                                                                                                                            class App extends Component {
                                                                                                                                state = {
                                                                                                                                    products: [
                                                                                                                                        { id: 1, name: 'Product 1', category: 'Category 1', price: 10, color: 'Red' },
                                                                                                                                        { id: 2, name: 'Product 2', category: 'Category 2', price: 20, color: 'Green' },
                                                                                                                                        { id: 3, name: 'Product 3', category: 'Category 1', price: 30, color: 'Blue' },
                                                                                                                                        { id: 4, name: 'Product 4', category: 'Category 2', price: 40, color: 'Red' },
                                                                                                                                        { id: 5, name: 'Product 5', category: 'Category 1', price: 50, color: 'Green' },
                                                                                                                                        { id: 6, name: 'Product 6', category: 'Category 2', price: 60, color: 'Blue' },
                                                                                                                                        { id: 7, name: 'Product 7', category: 'Category 1', price: 70, color: 'Red' },
                                                                                                                                        { id: 8, name: 'Product 8', category: 'Category 2', price: 80, color: 'Green' },
                                                                                                                                        { id: 9, name: 'Product 9', category: 'Category 1', price: 90, color: 'Blue' },
                                                                                                                                        { id: 10, name: 'Product 10', category: 'Category 2', price: 100, color: 'Red' },
                                                                                                                                    ],
                                                                                                                                    cart: [],
                                                                                                                                    sort: 'name-asc',
                                                                                                                                    filter: '',
                                                                                                                                    page: 1,
                                                                                                                                    productsPerPage: 4,
                                                                                                                                    showCart: false,
                                                                                                                                };

                                                                                                                                handleAddToCart = (product) => {
                                                                                                                                    const { cart } = this.state;
                                                                                                                                    const existingProductIndex = cart.findIndex((item) => item.id === product.id);
                                                                                                                                    if (existingProductIndex >= 0) {
                                                                                                                                        const updatedCart = [...cart];
                                                                                                                                        updatedCart[existingProductIndex].quantity += 1;
                                                                                                                                        this.setState({ cart: updatedCart });
                                                                                                                                    } else {
                                                                                                                                        const updatedCart = [...cart, { ...product, quantity: 1 }];
                                                                                                                                        this.setState({ cart: updatedCart });
                                                                                                                                    }
                                                                                                                                };

                                                                                                                                handleRemoveFromCart = (product) => {
                                                                                                                                    const { cart } = this.state;
                                                                                                                                    const existingProductIndex = cart.findIndex((item) => item.id === product.id);
                                                                                                                                    if (existingProductIndex >= 0) {
                                                                                                                                        const updatedCart = [...cart];
                                                                                                                                        if (updatedCart[existingProductIndex].quantity > 1) {
                                                                                                                                            updatedCart[existingProductIndex].quantity -= 1;
                                                                                                                                        } else {
                                                                                                                                            updatedCart.splice(existingProductIndex, 1);
                                                                                                                                        }
                                                                                                                                        this.setState({ cart: updatedCart });
                                                                                                                                    }
                                                                                                                                };

                                                                                                                                handleSortChange = (event) => {
                                                                                                                                    const { value } = event.target;
                                                                                                                                    const [a, b] = value.split('-');
                                                                                                                                    const bOrder = b === 'asc' ? 1 : -1;
                                                                                                                                    const sortedProducts = [...this.state.products].sort((productA, productB) => {
                                                                                                                                        if (productA[a] < productB[a]) {
                                                                                                                                            return -1 * bOrder;
                                                                                                                                        }
                                                                                                                                        if (productA[a] > productB[a]) {
                                                                                                                                            return 1 * bOrder;
                                                                                                                                        }
                                                                                                                                        return 0;
                                                                                                                                    });
                                                                                                                                    this.setState({ sort: value, products: sortedProducts });
                                                                                                                                };

                                                                                                                                handleFilterChange = (event) => {
                                                                                                                                    const { value } = event.target;
                                                                                                                                    this.setState({ filter: value });
                                                                                                                                };

                                                                                                                                handlePageChange = (event, page) => {
                                                                                                                                    event.preventDefault();
                                                                                                                                    this.setState({ page });
                                                                                                                                };

                                                                                                                                handleLoadMore = () => {
                                                                                                                                    this.setState((prevState) => ({ productsPerPage: prevState.productsPerPage + 4 }));
                                                                                                                                };

                                                                                                                                toggleCartVisibility = () => {
                                                                                                                                    this.setState((prevState) => ({ showCart: !prevState.showCart }));
                                                                                                                                };

                                                                                                                                render() {
                                                                                                                                    const { products, cart, sort, filter, page, productsPerPage, showCart } = this.state;

                                                                                                                                    const filteredData = products.filter((product) =>
                                                                                                                                        product.name.toLowerCase().includes(filter.toLowerCase())
                                                                                                                                    );

                                                                                                                                    const sortedData = [...filteredData].sort((productA, productB) => {
                                                                                                                                        const [a, b] = sort.split('-');
                                                                                                                                        const bOrder = b === 'asc' ? 1 : -1;
                                                                                                                                        if (productA[a] < productB[a]) {
                                                                                                                                            return -1 * bOrder;
                                                                                                                                        }
                                                                                                                                        if (productA[a] > productB[a]) {
                                                                                                                                            return 1 * bOrder;
                                                                                                                                        }
                                                                                                                                        return 0;
                                                                                                                                    });

                                                                                                                                    const paginatedData = sortedData.slice((page - 1) * productsPerPage, page * productsPerPage);

                                                                                                                                    const endIndex = page * productsPerPage;

                                                                                                                                    return (
                                                                                                                                        <div>
                                                                                                                                            <Header onFilterChange={this.handleFilterChange} filter={filter} cart={cart} toggleCartVisibility={this.toggleCartVisibility} />
                                                                                                                                            {showCart && (
                                                                                                                                                <div>
                                                                                                                                                    <h2>Cart</h2>
                                                                                                                                                    {cart.length === 0 ? (
                                                                                                                                                        <p>Your cart is empty</p>
                                                                                                                                                    ) : (
                                                                                                                                                        <ul>
                                                                                                                                                            import React, { Component } from 'react';
                                                                                                                                                            import ProductList from './ProductList';

                                                                                                                                                            class App extends Component {
                                                                                                                                                                state = {
                                                                                                                                                                    data: [],
                                                                                                                                                                    filteredData: [],
                                                                                                                                                                    sort: 'name-asc',
                                                                                                                                                                    cart: [],
                                                                                                                                                                    startIndex: 0,
                                                                                                                                                                    endIndex: 8,
                                                                                                                                                                };

                                                                                                                                                                componentDidMount() {
                                                                                                                                                                    fetch('https://fakestoreapi.com/products')
                                                                                                                                                                        .then((res) => res.json())
                                                                                                                                                                        .then((data) => this.setState({ data, filteredData: data }));
                                                                                                                                                                }

                                                                                                                                                                handleSortChange = (e) => {
                                                                                                                                                                    const { value } = e.target;
                                                                                                                                                                    const [field, order] = value.split('-');
                                                                                                                                                                    const sortedData = this.state.filteredData.sort((a, b) =>
                                                                                                                                                                        order === 'asc' ? a[field] - b[field] : b[field] - a[field]
                                                                                                                                                                    );
                                                                                                                                                                    this.setState({ sort: value, filteredData: sortedData });
                                                                                                                                                                };

                                                                                                                                                                handleAddToCart = (product) => {
                                                                                                                                                                    const { cart } = this.state;
                                                                                                                                                                    const existingProductIndex = cart.findIndex((item) => item.id === product.id);
                                                                                                                                                                    if (existingProductIndex !== -1) {
                                                                                                                                                                        const updatedCart = [...cart];
                                                                                                                                                                        updatedCart[existingProductIndex].quantity += 1;
                                                                                                                                                                        this.setState({ cart: updatedCart });
                                                                                                                                                                    } else {
                                                                                                                                                                        this.setState({ cart: [...cart, { ...product, quantity: 1 }] });
                                                                                                                                                                    }
                                                                                                                                                                };

                                                                                                                                                                handleRemoveFromCart = (product) => {
                                                                                                                                                                    const { cart } = this.state;
                                                                                                                                                                    const existingProductIndex = cart.findIndex((item) => item.id === product.id);
                                                                                                                                                                    if (existingProductIndex !== -1) {
                                                                                                                                                                        const updatedCart = [...cart];
                                                                                                                                                                        if (updatedCart[existingProductIndex].quantity > 1) {
                                                                                                                                                                            updatedCart[existingProductIndex].quantity -= 1;
                                                                                                                                                                            this.setState({ cart: updatedCart });
                                                                                                                                                                        } else {
                                                                                                                                                                            updatedCart.splice(existingProductIndex, 1);
                                                                                                                                                                            this.setState({ cart: updatedCart });
                                                                                                                                                                        }
                                                                                                                                                                    }
                                                                                                                                                                };

                                                                                                                                                                handleLoadMore = () => {
                                                                                                                                                                    this.setState((prevState) => ({
                                                                                                                                                                        startIndex: prevState.startIndex + 8,
                                                                                                                                                                        endIndex: prevState.endIndex + 8,
                                                                                                                                                                    }));
                                                                                                                                                                };

                                                                                                                                                                render() {
                                                                                                                                                                    const { filteredData, sort, cart, startIndex, endIndex } = this.state;
                                                                                                                                                                    const paginatedData = filteredData.slice(startIndex, endIndex);

                                                                                                                                                                    return (
                                                                                                                                                                        <div>
                                                                                                                                                                            <div>
                                                                                                                                                                                <h1>Product Listing Page</h1>
                                                                                                                                                                                <ul>
                                                                                                                                                                                    {cart.map((item) => (
                                                                                                                                                                                        <li key={item.id}>
                                                                                                                                                                                            {item.name} x {item.quantity} - ${item.price * item.quantity}
                                                                                                                                                                                            import React, { Component } from 'react';
                                                                                                                                                                                            import ProductList from './ProductList';

                                                                                                                                                                                            class App extends Component {
                                                                                                                                                                                                constructor(props) {
                                                                                                                                                                                                    super(props);
                                                                                                                                                                                                    this.state = {
                                                                                                                                                                                                        data: [],
                                                                                                                                                                                                        cart: [],
                                                                                                                                                                                                        sort: 'name-asc',
                                                                                                                                                                                                        startIndex: 0,
                                                                                                                                                                                                        endIndex: 10,
                                                                                                                                                                                                        searchTerm: '',
                                                                                                                                                                                                    };
                                                                                                                                                                                                }

                                                                                                                                                                                                componentDidMount() {
                                                                                                                                                                                                    fetch('https://fakestoreapi.com/products')
                                                                                                                                                                                                        .then((response) => response.json())
                                                                                                                                                                                                        .then((data) => this.setState({ data }));
                                                                                                                                                                                                }

                                                                                                                                                                                                handleAddToCart = (product) => {
                                                                                                                                                                                                    this.setState((prevState) => ({
                                                                                                                                                                                                        cart: [...prevState.cart, product],
                                                                                                                                                                                                    }));
                                                                                                                                                                                                };

                                                                                                                                                                                                handleRemoveFromCart = (product) => {
                                                                                                                                                                                                    this.setState((prevState) => ({
                                                                                                                                                                                                        cart: prevState.cart.filter((item) => item.id !== product.id),
                                                                                                                                                                                                    }));
                                                                                                                                                                                                };

                                                                                                                                                                                                handleSortChange = (event) => {
                                                                                                                                                                                                    this.setState({ sort: event.target.value });
                                                                                                                                                                                                };

                                                                                                                                                                                                handleLoadMore = () => {
                                                                                                                                                                                                    this.setState((prevState) => ({
                                                                                                                                                                                                        startIndex: prevState.startIndex + 10,
                                                                                                                                                                                                        endIndex: prevState.endIndex + 10,
                                                                                                                                                                                                    }));
                                                                                                                                                                                                };

                                                                                                                                                                                                handleSearchChange = (event) => {
                                                                                                                                                                                                    this.setState({ searchTerm: event.target.value });
                                                                                                                                                                                                };

                                                                                                                                                                                                render() {
                                                                                                                                                                                                    const { data, cart, sort, startIndex, endIndex, searchTerm } = this.state;

                                                                                                                                                                                                    const filteredData = data.filter((item) =>
                                                                                                                                                                                                        item.title.toLowerCase().includes(searchTerm.toLowerCase())
                                                                                                                                                                                                    );

                                                                                                                                                                                                    const sortedData = filteredData.sort((a, b) => {
                                                                                                                                                                                                        const [aKey, aDirection] = sort.split('-');
                                                                                                                                                                                                        const [bKey, bDirection] = sort.split('-');
                                                                                                                                                                                                        if (a[aKey] < b[bKey]) {
                                                                                                                                                                                                            return aDirection === 'asc' ? -1 : 1;
                                                                                                                                                                                                        }
                                                                                                                                                                                                        if (a[aKey] > b[bKey]) {
                                                                                                                                                                                                            return aDirection === 'asc' ? 1 : -1;
                                                                                                                                                                                                        }
                                                                                                                                                                                                        return 0;
                                                                                                                                                                                                    });

                                                                                                                                                                                                    const paginatedData = sortedData.slice(startIndex, endIndex);

                                                                                                                                                                                                    return (
                                                                                                                                                                                                        <div>
                                                                                                                                                                                                            <header style={{ position: 'fixed', top: 0 }}>
                                                                                                                                                                                                                <h1>Product Listing Page</h1>
                                                                                                                                                                                                                <div>
                                                                                                                                                                                                                    <label htmlFor="search">Search</label>
                                                                                                                                                                                                                    <input type="text" id="search" value={searchTerm} onChange={this.handleSearchChange} />
                                                                                                                                                                                                                </div>
                                                                                                                                                                                                                <div>
                                                                                                                                                                                                                    <p>Cart ({cart.length})</p>
                                                                                                                                                                                                                </div>
                                                                                                                                                                                                            </header>
                                                                                                                                                                                                            <div style={{ paddingTop: '100px' }}>
                                                                                                                                                                                                                <div>
                                                                                                                                                                                                                    <ul>
                                                                                                                                                                                                                        {paginatedData.map((item) => (
                                                                                                                                                                                                                            <li key={item.id}>
                                                                                                                                                                                                                                <h2>{item.title}</h2>
                                                                                                                                                                                                                                <p>{item.description}</p>
                                                                                                                                                                                                                                <p>${item.price}</p>
                                                                                                                                                                                                                                <button onClick={() => this.handleAddToCart(item)}>Add to cart</button>
                                                                                                                                                                                                                                <button onClick={() => this.handleRemoveFromCart(item)}>Remove</button>
                                                                                                                                                                                                                            </li>
                                                                                                                                                                                                                        ))}
                                                                                                                                                                                                                    </ul>
                                                                                                                                                                                                                </div>
                                                                                                                                                                                                                import React, { Component } from 'react';
                                                                                                                                                                                                                import ProductList from './ProductList';

                                                                                                                                                                                                                class App extends Component {
                                                                                                                                                                                                                    constructor(props) {
                                                                                                                                                                                                                        super(props);
                                                                                                                                                                                                                        this.state = {
                                                                                                                                                                                                                            data: props.products,
                                                                                                                                                                                                                            cart: [],
                                                                                                                                                                                                                            sort: 'name-asc',
                                                                                                                                                                                                                            filters: [],
                                                                                                                                                                                                                            startIndex: 0,
                                                                                                                                                                                                                            endIndex: 10,
                                                                                                                                                                                                                        };
                                                                                                                                                                                                                        this.handleAddToCart = this.handleAddToCart.bind(this);
                                                                                                                                                                                                                        this.handleRemoveFromCart = this.handleRemoveFromCart.bind(this);
                                                                                                                                                                                                                        this.handleSortChange = this.handleSortChange.bind(this);
                                                                                                                                                                                                                        this.handleFilterChange = this.handleFilterChange.bind(this);
                                                                                                                                                                                                                        this.handleLoadMore = this.handleLoadMore.bind(this);
                                                                                                                                                                                                                    }

                                                                                                                                                                                                                    handleAddToCart(product) {
                                                                                                                                                                                                                        this.setState((prevState) => ({
                                                                                                                                                                                                                            cart: [...prevState.cart, product],
                                                                                                                                                                                                                        }));
                                                                                                                                                                                                                    }

                                                                                                                                                                                                                    handleRemoveFromCart(product) {
                                                                                                                                                                                                                        this.setState((prevState) => ({
                                                                                                                                                                                                                            cart: prevState.cart.filter((p) => p.id !== product.id),
                                                                                                                                                                                                                        }));
                                                                                                                                                                                                                    }

                                                                                                                                                                                                                    handleSortChange(event) {
                                                                                                                                                                                                                        this.setState({ sort: event.target.value });
                                                                                                                                                                                                                    }

                                                                                                                                                                                                                    handleFilterChange(event) {
                                                                                                                                                                                                                        const { value, checked } = event.target;
                                                                                                                                                                                                                        this.setState((prevState) => {
                                                                                                                                                                                                                            let filters = [...prevState.filters];
                                                                                                                                                                                                                            if (checked) {
                                                                                                                                                                                                                                filters.push(value);
                                                                                                                                                                                                                            } else {
                                                                                                                                                                                                                                filters = filters.filter((f) => f !== value);
                                                                                                                                                                                                                            }
                                                                                                                                                                                                                            return { filters };
                                                                                                                                                                                                                        });
                                                                                                                                                                                                                    }

                                                                                                                                                                                                                    handleLoadMore() {
                                                                                                                                                                                                                        this.setState((prevState) => ({
                                                                                                                                                                                                                            startIndex: prevState.startIndex + 10,
                                                                                                                                                                                                                            endIndex: prevState.endIndex + 10,
                                                                                                                                                                                                                        }));
                                                                                                                                                                                                                    }

                                                                                                                                                                                                                    render() {
                                                                                                                                                                                                                        const { data, cart, sort, filters, startIndex, endIndex } = this.state;
                                                                                                                                                                                                                        const filteredData = data.filter((product) => {
                                                                                                                                                                                                                            if (filters.length === 0) {
                                                                                                                                                                                                                                return true;
                                                                                                                                                                                                                            }
                                                                                                                                                                                                                            return filters.includes(product.category);
                                                                                                                                                                                                                        });
                                                                                                                                                                                                                        const sortedData = filteredData.sort((a, b) => {
                                                                                                                                                                                                                            const [aKey, aOrder] = sort.split('-');
                                                                                                                                                                                                                            const [bKey, bOrder] = sort.split('-');
                                                                                                                                                                                                                            if (a[aKey] < b[bKey]) {
                                                                                                                                                                                                                                return aOrder === 'asc' ? -1 : 1;
                                                                                                                                                                                                                            }
                                                                                                                                                                                                                            if (a[aKey] > b[bKey]) {
                                                                                                                                                                                                                                return aOrder === 'asc' ? 1 : -1;
                                                                                                                                                                                                                            }
                                                                                                                                                                                                                            return 0;
                                                                                                                                                                                                                        });
                                                                                                                                                                                                                        const paginatedData = sortedData.slice(startIndex, endIndex);

                                                                                                                                                                                                                        return (
                                                                                                                                                                                                                            <div>
                                                                                                                                                                                                                                <div>
                                                                                                                                                                                                                                    <p>Showing {filteredData.length} products</p>
                                                                                                                                                                                                                                    <div>
                                                                                                                                                                                                                                        <label htmlFor="sort">Sort by</label>
                                                                                                                                                                                                                                        <select id="sort" value={sort} onChange={this.handleSortChange}>
                                                                                                                                                                                                                                            <option value="name-asc">Name (Ascending)</option>
                                                                                                                                                                                                                                            <option value="name-desc">Name (Descending)</option>
                                                                                                                                                                                                                                            <option value="price-asc">Price (Ascending)</option>
                                                                                                                                                                                                                                            <option value="price-desc">Price (Descending)</option>
                                                                                                                                                                                                                                        </select>
                                                                                                                                                                                                                                    </div>
                                                                                                                                                                                                                                    <div>
                                                                                                                                                                                                                                        <p>Filter by category:</p>
                                                                                                                                                                                                                                        <label htmlFor="filter1">
                                                                                                                                                                                                                                            <input type="checkbox" id="filter1" value="electronics" onChange={this.handleFilterChange} checked={filters.includes('electronics')} />
                                                                                                                                                                                                                                            import React, { Component } from 'react';
                                                                                                                                                                                                                                            import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
                                                                                                                                                                                                                                            import { faShoppingCart } from '@fortawesome/free-solid-svg-icons';
                                                                                                                                                                                                                                            import Header from './Header';
                                                                                                                                                                                                                                            import ProductList from './ProductList';

                                                                                                                                                                                                                                            class App extends Component {
                                                                                                                                                                                                                                                constructor(props) {
                                                                                                                                                                                                                                                    super(props);
                                                                                                                                                                                                                                                    this.state = {
                                                                                                                                                                                                                                                        products: [
                                                                                                                                                                                                                                                            { id: 1, name: 'iPhone', category: 'electronics', price: 500 },
                                                                                                                                                                                                                                                            { id: 2, name: 'Samsung', category: 'electronics', price: 400 },
                                                                                                                                                                                                                                                            { id: 3, name: 'LG', category: 'electronics', price: 300 },
                                                                                                                                                                                                                                                            { id: 4, name: 'Levi\'s', category: 'clothing', price: 50 },
                                                                                                                                                                                                                                                            { id: 5, name: 'Lee', category: 'clothing', price: 40 },
                                                                                                                                                                                                                                                            { id: 6, name: 'Wrangler', category: 'clothing', price: 30 },
                                                                                                                                                                                                                                                            { id: 7, name: 'The Catcher in the Rye', category: 'books', price: 10 },
                                                                                                                                                                                                                                                            { id: 8, name: 'To Kill a Mockingbird', category: 'books', price: 12 },
                                                                                                                                                                                                                                                            { id: 9, name: '1984', category: 'books', price: 15 }
                                                                                                                                                                                                                                                        ],
                                                                                                                                                                                                                                                        cart: []
                                                                                                                                                                                                                                                    };
                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                handleAddToCart = (product) => {
                                                                                                                                                                                                                                                    const { cart } = this.state;
                                                                                                                                                                                                                                                    const existingProductIndex = cart.findIndex(p => p.id === product.id);
                                                                                                                                                                                                                                                    if (existingProductIndex !== -1) {
                                                                                                                                                                                                                                                        const updatedCart = [...cart];
                                                                                                                                                                                                                                                        updatedCart[existingProductIndex].quantity += 1;
                                                                                                                                                                                                                                                        this.setState({ cart: updatedCart });
                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                        const updatedProduct = { ...product, quantity: 1 };
                                                                                                                                                                                                                                                        this.setState({ cart: [...cart, updatedProduct] });
                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                handleRemoveFromCart = (product) => {
                                                                                                                                                                                                                                                    const { cart } = this.state;
                                                                                                                                                                                                                                                    const existingProductIndex = cart.findIndex(p => p.id === product.id);
                                                                                                                                                                                                                                                    if (existingProductIndex !== -1) {
                                                                                                                                                                                                                                                        const updatedCart = [...cart];
                                                                                                                                                                                                                                                        if (updatedCart[existingProductIndex].quantity > 1) {
                                                                                                                                                                                                                                                            updatedCart[existingProductIndex].quantity -= 1;
                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                            updatedCart.splice(existingProductIndex, 1);
                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                        this.setState({ cart: updatedCart });
                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                handleFilterChange = (event) => {
                                                                                                                                                                                                                                                    const { value, checked } = event.target;
                                                                                                                                                                                                                                                    const { filters } = this.state;
                                                                                                                                                                                                                                                    if (checked) {
                                                                                                                                                                                                                                                        this.setState({ filters: [...filters, value] });
                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                        const updatedFilters = filters.filter(f => f !== value);
                                                                                                                                                                                                                                                        this.setState({ filters: updatedFilters });
                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                handleSortChange = (event) => {
                                                                                                                                                                                                                                                    const { value } = event.target;
                                                                                                                                                                                                                                                    this.setState({ sort: value });
                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                handlePageChange = (event) => {
                                                                                                                                                                                                                                                    const { value } = event.target;
                                                                                                                                                                                                                                                    this.setState({ page: Number(value) });
                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                handleLoadMore = () => {
                                                                                                                                                                                                                                                    const { productsPerPage } = this.props;
                                                                                                                                                                                                                                                    this.setState(prevState => ({ productsPerPage: prevState.productsPerPage + productsPerPage }));
                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                render() {
                                                                                                                                                                                                                                                    const { products, cart, filters, sort, page, productsPerPage } = this.state;

                                                                                                                                                                                                                                                    // filter products
                                                                                                                                                                                                                                                    let filteredData = products.filter(product => filters.includes(product.category));

                                                                                                                                                                                                                                                    // sort products
                                                                                                                                                                                                                                                    if (sort === 'priceAsc') {
                                                                                                                                                                                                                                                        filteredData = filteredData.sort((a, b) => a.price - b.price);
                                                                                                                                                                                                                                                    } else if (sort === 'priceDesc') {
                                                                                                                                                                                                                                                        filteredData = filteredData.sort((a, b) => b.price - a.price);
                                                                                                                                                                                                                                                    }

                                                                                                                                                                                                                                                    // paginate products
                                                                                                                                                                                                                                                    const startIndex = (page - 1) * productsPerPage;
                                                                                                                                                                                                                                                    const endIndex = startIndex + productsPerPage;
                                                                                                                                                                                                                                                    const paginatedData = filteredData.slice(startIndex, endIndex);

                                                                                                                                                                                                                                                    return (
                                                                                                                                                                                                                                                        <div>
                                                                                                                                                                                                                                                            <Header />
                                                                                                                                                                                                                                                            <div>
                                                                                                                                                                                                                                                                <ul>
                                                                                                                                                                                                                                                                    <li>
                                                                                                                                                                                                                                                                        <label htmlFor="sort">
                                                                                                                                                                                                                                                                            Sort by:
                                                                                                                                                                                                                                                                            <select id="sort" value={sort} onChange={this.handleSortChange}>
                                                                                                                                                                                                                                                                                <option value="priceAsc">Price: Low to High</option>
                                                                                                                                                                                                                                                                                <option value="priceDesc">Price: High to Low</option>
                                                                                                                                                                                                                                                                            </select>
                                                                                                                                                                                                                                                                        </label>
                                                                                                                                                                                                                                                                    </li>
                                                                                                                                                                                                                                                                    <li>
                                                                                                                                                                                                                                                                        <label htmlFor="filter1">
                                                                                                                                                                                                                                                                            <input type="checkbox" id="filter1" value="electronics" onChange={this.handleFilterChange} checked={filters.includes('electronics')} />
                                                                                                                                                                                                                                                                            Electronics
                                                                                                                                                                                                                                                                        </label>
                                                                                                                                                                                                                                                                    </li>
                                                                                                                                                                                                                                                                    <li>
                                                                                                                                                                                                                                                                        <label htmlFor="filter2">
                                                                                                                                                                                                                                                                            <input type="checkbox" id="filter2" value="clothing" onChange={this.handleFilterChange} checked={filters.includes('clothing')} />
                                                                                                                                                                                                                                                                            Clothing
                                                                                                                                                                                                                                                                        </label>
                                                                                                                                                                                                                                                                    </li>
                                                                                                                                                                                                                                                                    <li>
                                                                                                                                                                                                                                                                        <label htmlFor="filter3">
                                                                                                                                                                                                                                                                            import React, { Component } from 'react';
                                                                                                                                                                                                                                                                            import ProductList from './ProductList';
                                                                                                                                                                                                                                                                            import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
                                                                                                                                                                                                                                                                            import { faShoppingCart } from '@fortawesome/free-solid-svg-icons';

                                                                                                                                                                                                                                                                            class App extends Component {
                                                                                                                                                                                                                                                                                constructor(props) {
                                                                                                                                                                                                                                                                                    super(props);
                                                                                                                                                                                                                                                                                    this.state = {
                                                                                                                                                                                                                                                                                        data: [],
                                                                                                                                                                                                                                                                                        cart: [],
                                                                                                                                                                                                                                                                                        filters: [],
                                                                                                                                                                                                                                                                                        filteredData: [],
                                                                                                                                                                                                                                                                                        startIndex: 0,
                                                                                                                                                                                                                                                                                        endIndex: 6,
                                                                                                                                                                                                                                                                                    };
                                                                                                                                                                                                                                                                                    this.handleAddToCart = this.handleAddToCart.bind(this);
                                                                                                                                                                                                                                                                                    this.handleRemoveFromCart = this.handleRemoveFromCart.bind(this);
                                                                                                                                                                                                                                                                                    this.handleFilterChange = this.handleFilterChange.bind(this);
                                                                                                                                                                                                                                                                                    this.handleLoadMore = this.handleLoadMore.bind(this);
                                                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                                                componentDidMount() {
                                                                                                                                                                                                                                                                                    fetch('https://fakestoreapi.com/products')
                                                                                                                                                                                                                                                                                        .then((response) => response.json())
                                                                                                                                                                                                                                                                                        .then((data) => {
                                                                                                                                                                                                                                                                                            this.setState({ data, filteredData: data });
                                                                                                                                                                                                                                                                                        });
                                                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                                                handleAddToCart(product) {
                                                                                                                                                                                                                                                                                    const { cart } = this.state;
                                                                                                                                                                                                                                                                                    const existingProductIndex = cart.findIndex((p) => p.id === product.id);
                                                                                                                                                                                                                                                                                    if (existingProductIndex >= 0) {
                                                                                                                                                                                                                                                                                        const cartCopy = [...cart];
                                                                                                                                                                                                                                                                                        cartCopy[existingProductIndex].quantity += 1;
                                                                                                                                                                                                                                                                                        this.setState({ cart: cartCopy });
                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                        this.setState({ cart: [...cart, { ...product, quantity: 1 }] });
                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                                                handleRemoveFromCart(product) {
                                                                                                                                                                                                                                                                                    const { cart } = this.state;
                                                                                                                                                                                                                                                                                    const existingProductIndex = cart.findIndex((p) => p.id === product.id);
                                                                                                                                                                                                                                                                                    if (existingProductIndex >= 0) {
                                                                                                                                                                                                                                                                                        const cartCopy = [...cart];
                                                                                                                                                                                                                                                                                        if (cartCopy[existingProductIndex].quantity > 1) {
                                                                                                                                                                                                                                                                                            cartCopy[existingProductIndex].quantity -= 1;
                                                                                                                                                                                                                                                                                            this.setState({ cart: cartCopy });
                                                                                                                                                                                                                                                                                        } else {
                                                                                                                                                                                                                                                                                            cartCopy.splice(existingProductIndex, 1);
                                                                                                                                                                                                                                                                                            this.setState({ cart: cartCopy });
                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                                                handleFilterChange(event) {
                                                                                                                                                                                                                                                                                    const { filters } = this.state;
                                                                                                                                                                                                                                                                                    const { value } = event.target;
                                                                                                                                                                                                                                                                                    if (filters.includes(value)) {
                                                                                                                                                                                                                                                                                        const filtersCopy = [...filters];
                                                                                                                                                                                                                                                                                        filtersCopy.splice(filtersCopy.indexOf(value), 1);
                                                                                                                                                                                                                                                                                        this.setState({ filters: filtersCopy }, this.filterData);
                                                                                                                                                                                                                                                                                    } else {
                                                                                                                                                                                                                                                                                        this.setState({ filters: [...filters, value] }, this.filterData);
                                                                                                                                                                                                                                                                                    }
                                                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                                                filterData() {
                                                                                                                                                                                                                                                                                    const { data, filters } = this.state;
                                                                                                                                                                                                                                                                                    const filteredData = data.filter((product) => filters.includes(product.category));
                                                                                                                                                                                                                                                                                    this.setState({ filteredData, startIndex: 0, endIndex: 6 });
                                                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                                                handleLoadMore() {
                                                                                                                                                                                                                                                                                    this.setState((prevState) => ({
                                                                                                                                                                                                                                                                                        endIndex: prevState.endIndex + 6,
                                                                                                                                                                                                                                                                                    }));
                                                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                                                render() {
                                                                                                                                                                                                                                                                                    const { filteredData, startIndex, endIndex, cart, filters } = this.state;
                                                                                                                                                                                                                                                                                    const paginatedData = filteredData.slice(startIndex, endIndex);
                                                                                                                                                                                                                                                                                    return (
                                                                                                                                                                                                                                                                                        <div>
                                                                                                                                                                                                                                                                                            <div>
                                                                                                                                                                                                                                                                                                <ul>
                                                                                                                                                                                                                                                                                                    <li>
                                                                                                                                                                                                                                                                                                        <label htmlFor="filter1">
                                                                                                                                                                                                                                                                                                            <input type="checkbox" id="filter1" value="electronics" onChange={this.handleFilterChange} checked={filters.includes('electronics')} />
                                                                                                                                                                                                                                                                                                            Electronics
                                                                                                                                                                                                                                                                                                        </label>
                                                                                                                                                                                                                                                                                                    </li>
                                                                                                                                                                                                                                                                                                    <li>
                                                                                                                                                                                                                                                                                                        <label htmlFor="filter2">
                                                                                                                                                                                                                                                                                                            <input type="checkbox" id="filter2" value="jewelery" onChange={this.handleFilterChange} checked={filters.includes('jewelery')} />
                                                                                                                                                                                                                                                                                                            Jewelery
                                                                                                                                                                                                                                                                                                        </label>
                                                                                                                                                                                                                                                                                                    </li>
                                                                                                                                                                                                                                                                                                    <li>
                                                                                                                                                                                                                                                                                                        <label htmlFor="filter3">
                                                                                                                                                                                                                                                                                                            <input type="checkbox" id="filter3" value="books" onChange={this.handleFilterChange} checked={filters.includes('books')} />
                                                                                                                                                                                                                                                                                                            Books
                                                                                                                                                                                                                                                                                                        </label>
                                                                                                                                                                                                                                                                                                    </li>
                                                                                                                                                                                                                                                                                                </ul>
                                                                                                                                                                                                                                                                                            </div>
                                                                                                                                                                                                                                                                                            <div>
                                                                                                                                                                                                                                                                                                <ProductList products={paginatedData} onAddToCart={this.handleAddToCart} onRemoveFromCart={this.handleRemoveFromCart} cart={cart} />
                                                                                                                                                                                                                                                                                            </div>
                                                                                                                                                                                                                                                                                            {filteredData.length > endIndex && <button onClick={this.handleLoadMore}>Load more</button>}
                                                                                                                                                                                                                                                                                            <div>
                                                                                                                                                                                                                                                                                                <FontAwesomeIcon icon={faShoppingCart} />
                                                                                                                                                                                                                                                                                                <span>{cart.reduce((total, product) => total + product.quantity, 0)}</span>
                                                                                                                                                                                                                                                                                            </div>
                                                                                                                                                                                                                                                                                            <footer>
                                                                                                                                                                                                                                                                                                <ul>
                                                                                                                                                                                                                                                                                                    <li><a href="#">Home</a></li>
                                                                                                                                                                                                                                                                                                    <li><a href="#">About Us</a></li>
                                                                                                                                                                                                                                                                                                    <li><a href="#">Contact Us</a></li>
                                                                                                                                                                                                                                                                                                </ul>
                                                                                                                                                                                                                                                                                            </footer>
                                                                                                                                                                                                                                                                                        </div>
                                                                                                                                                                                                                                                                                    );
                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                            }

                                                                                                                                                                                                                                                                            export default App;
