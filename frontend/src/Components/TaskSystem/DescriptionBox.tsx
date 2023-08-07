import { FunctionComponent } from 'react';
import styles from './DescriptionBox.module.css';

const DescriptionBox: FunctionComponent<{ children: React.ReactNode }> = ({ children }) => {
    if (!children) {
        children = "Description Text";
    }
    return (
        <div className={styles.descriptionBox}>
            <div className={styles.listboxbg} />
            <div className={styles.descriptionText1}>{children}</div>
        </div>);
};

export default DescriptionBox;
