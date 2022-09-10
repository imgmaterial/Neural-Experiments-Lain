import React, { FC } from 'react';

const About: FC = () => {
  const paragraphStyles: string = 'text-gray-600 mb-4 text-[0.9rem]';
  const spanStyles: string = 'font-bold';
  return (
    <main>
      <section className='container mx-auto min-h-[calc(100vh-60px)] flex justify-center items-center'>
        <section className='max-w-[820px] mx-auto my-2'>
          <section className='px-8 py-4 shadow-sm rounded-xl shadow-slate-800 last:mb-0 flex flex-col'>
            <h1 className='my-2 pb-2 font-extrabold text-gray-600 text-bold text-xl border-b-2'>
              About this project
            </h1>
            <h3 className='text-blue-500 cursor-pointer hover:underline text-lg font-mono uppercase mb-1 pl-3'>
              Neural Experiments Lain
            </h3>
            <p className={paragraphStyles}>
              <span className={spanStyles}>Neural Experiments</span> is an anime
              recommendation system based on collaborative learning for neural
              networks. The project relies on FastAIs implementation of
              collaborative learning model. For the user this means that the
              recommendations given by the neural network rely not on the
              contents or attributes of the recommended title but on the
              interactions of users that have shown to have a similar taste in
              anime as the user did. A preexisting data set of MyAnimeList user
              ratings was used to train the model and the model is continuously
              being trained as information is received from new users and new
              shows come out.
            </p>

            <p className={paragraphStyles}>
              In order to use the recommendation system the user needs to enter
              into the database a set of previously watched titles along with a
              rating on scale of 1-10. Ability to authenticate through some of
              the already existing anime list sites would be implemented in the
              future to make the process smoother for users who already have a
              large collection of anime listed on a third party platform. The
              relevant information from the entries is then sent into our
              database for the model to further learn from them and the user
              will be able to request a list of 10 top recommendations from the
              neural networks perspective.
            </p>
            <button className='mr-4 px-4 py-2  text-white bg-gray-500 border-slate-700 rounded-sm hover:bg-gray-600 self-end grow-0 hover:outline-3'>
              Get started
            </button>
          </section>
        </section>
      </section>
    </main>
  );
};

export default About;
