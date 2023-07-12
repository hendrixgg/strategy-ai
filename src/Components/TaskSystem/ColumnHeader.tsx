import { FunctionComponent } from 'react';
import styles from './ColumnHeader.module.css';
const ColumnHeader: FunctionComponent<{ titleText: string }> = ({ titleText }) => {

    return (
        <div className={styles.columnHeader}>
            <h2>{titleText}</h2>
        </div>);
};

export default ColumnHeader;
