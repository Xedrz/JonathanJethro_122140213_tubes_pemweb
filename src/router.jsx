// App.jsx
import { AuthProvider } from './context/AuthContext';
import AppRouter from './router';  // Mengimpor router.jsx yang berisi konfigurasi routing

function App() {
  return (
    <AuthProvider>
      <AppRouter />
    </AuthProvider>
  );
}

export default App;
