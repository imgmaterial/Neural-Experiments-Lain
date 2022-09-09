import React from 'react';

function Navbar() {
  return (
    <>
      <nav className='w-full h-[60px] pl-5 sticky top-0 left-0 bg-gray-800 flex items-center justify-between '>
        <h1 className='text-2xl text-white cursor-pointer select-none'>NEL</h1>
      </nav>
    </>
  );
}

export default Navbar;
