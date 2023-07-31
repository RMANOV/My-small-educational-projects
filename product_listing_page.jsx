import React, { useState, useEffect } from 'react';
import CSSModules from 'react-css-modules';
import styles from './App.module.css';
import Product from './Product';
import Header from './Header';
import ProductGrid from './ProductGrid';
import Filter from './Filter';
import Sort from './Sort';
import LoadMore from './LoadMore';
import Footer from './Footer';

const productData = require('./data.json');

const App = () => {
    const [products, setProducts] = useState(productData);
    const [displayedProducts, setDisplayedProducts] = useState([]);
    const [filters, setFilters] = useState({
        color: '',
        price: '',
    });
    const [sort, setSort] = useState('none');

    useEffect(() => {
        setDisplayedProducts(products);
    }, [filters, sort]);

    return (
        <div style={styles.div}>
            <Header />
            <ProductGrid products={displayedProducts} />
            <Filter filters={filters} setFilters={setFilters} />
            <Sort sort={sort} setSort={setSort} />
            <LoadMore />
            <Footer />
        </div>
    );
};

export default CSSModules(App, styles);
