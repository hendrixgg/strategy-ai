import React, { FunctionComponent } from 'react';
import styles from './Button.module.css';
const Button: FunctionComponent<{ disabled: boolean, children: React.ReactNode }> = ({ disabled, children }) => {

    return (
        <button className={styles.buttonMaster} disabled={disabled}>
            {children}
        </button>
    );
};

export default Button;
