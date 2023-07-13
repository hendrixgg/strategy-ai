import React, { FunctionComponent } from 'react';
import styles from './Clickable.module.css';
const Button: FunctionComponent<{ onClick: Function, disabled: boolean, children: React.ReactNode }> = ({ onClick, disabled, children }) => {

    return (
        <div className={disabled ? styles.disabled : styles.clickable} onClick={() => onClick()}>
            {children}
        </div>
    );
};

export default Button;
