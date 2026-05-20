import { AuthProvider } from "./contexts/AuthContext";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";

import Navbar from "./components/Navbar";

import HomePage from "./pages/HomePage";
import ExplorePage from "./pages/ExplorePage";
import DestinationDetailPage from "./pages/DestinationDetailPage";
import PlannerPage from "./pages/PlannerPage";
import BudgetPlannerPage from "./pages/BudgetPlannerPage";
import FestivalsPage from "./pages/FestivalsPage";
import ProfilePage from "./pages/ProfilePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import NotFoundPage from "./pages/NotFoundPage";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="flex flex-col min-h-screen bg-background">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/explore" element={<ExplorePage />} />
              <Route path="/destinations/:id" element={<DestinationDetailPage />} />
              <Route path="/planner" element={<ProtectedRoute><PlannerPage /></ProtectedRoute>} />
              <Route path="/planner/:id/budget" element={<ProtectedRoute><BudgetPlannerPage /></ProtectedRoute>} />
              <Route path="/festivals" element={<FestivalsPage />} />
              <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
