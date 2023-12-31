import { FunctionComponent, useState } from 'react';
import styles from './DropDownList.module.css';
import { Task } from './Tasks';

const DropDownList: FunctionComponent<{
    setTask: Function,
    selectedOption: Task,
    options: Array<Task>,
    disabled: boolean,
}> = ({ setTask, selectedOption, options, disabled }) => {
    const [open, setOpen] = useState<boolean>(false);
    const disabledFilter = (func: any) => {
        if (!disabled) {
            return func;
        } else {
            return () => { setOpen(false) };
        }
    }
    const selectOption = (option: Task) => {
        setTask(option);
        setOpen(false);
    }
    return (
        <>
            <div className={styles.clipList}>
                <div role="button" className={styles.listboxHeadCurrent} onClick={disabledFilter(() => setOpen(!open))}>
                    <div className={styles.listboxbg} />
                    <div className={styles.selectTask}>{selectedOption.name}</div>
                    <img className={styles.chevronIcon3} alt="" src="Chevron.svg" />
                </div>
                {open &&
                    <div className={styles.dropdownList}>
                        {options.map((option) => {
                            return (
                                <div role="button" key={option.id} className={styles.item1} onClick={disabledFilter(() => selectOption(option))}>
                                    <div className={styles.div}>{option.name}</div>
                                </div>
                            );
                        })}
                    </div>}
            </div>
        </>);
};

export default DropDownList;
