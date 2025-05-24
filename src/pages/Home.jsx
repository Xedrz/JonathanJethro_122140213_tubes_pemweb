import React from 'react';

export default function Home() {
  const token = localStorage.getItem('token');

  return (
    <div className="text-center mt-20">
      <h1 className="text-3xl font-bold">Selamat Datang di Bukuku</h1>
      {token ? (
        <p className="mt-4 text-green-600">Kamu sudah login 🎉</p>
      ) : (
        <p className="mt-4 text-gray-600">Silakan login atau register</p>
      )}
    </div>
  );
}
