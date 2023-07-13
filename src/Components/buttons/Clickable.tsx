import React, { FunctionComponent } from 'react';
import styles from './Clickable.module.css';
const Button: FunctionComponent<{ onClick: Function, disabled: boolean, children: React.ReactNode }> = ({ onClick, disabled, children }) => {

    return (
        <button className={styles.clickable} disabled={disabled} onClick={() => onClick()}>
            {children}
        </button>
    );
};

export default Button;
