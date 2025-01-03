import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private tokenKey = 'authToken';
  private preTokenKey = 'preAuthToken';

  isLoggedIn(): boolean {
    const token = localStorage.getItem(this.tokenKey) || sessionStorage.getItem(this.tokenKey);
    return !!token;
  }

  getToken(): string | null {
    return sessionStorage.getItem(this.tokenKey);
  }

  getPreToken(): string | null {
    return sessionStorage.getItem(this.preTokenKey);
  }

  setToken(token: string): void {
    sessionStorage.setItem(this.tokenKey, token);
  }

  setPreToken(token: string): void {
    sessionStorage.setItem(this.preTokenKey, token);
  }

  clearToken(): void {
    sessionStorage.removeItem(this.tokenKey);
    sessionStorage.removeItem(this.preTokenKey);
  }

  setFromPreToken(): void {
    const token = this.getPreToken()
    if (token) this.setToken(token)
  }
}
