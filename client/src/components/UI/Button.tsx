import React, { FC } from 'react';

interface IButtonProps {
  children?: React.ReactNode;
  props: {
    onClick: () => void;
  };
}

const Button: FC<IButtonProps> = ({ children, props }) => {
  return <button {...props}>{children}</button>;
};
export default Button;
