import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private tokenKey = 'authToken';
  private loggedInKey = 'loggedIn';

  isLoggedIn(): boolean {
    const token = localStorage.getItem(this.tokenKey) || sessionStorage.getItem(this.tokenKey);
    const loggedIn = JSON.parse(sessionStorage.getItem(this.loggedInKey) || 'false');
    return (!!token && loggedIn);
  }

  setLoggedIn(loggedIn: boolean) {
    sessionStorage.setItem(this.loggedInKey, JSON.stringify(loggedIn));
  }

  getToken(): string | null {
    return sessionStorage.getItem(this.tokenKey);
  }

  setToken(token: string): void {
    sessionStorage.setItem(this.tokenKey, token);
  }

  clearToken(): void {
    sessionStorage.removeItem(this.loggedInKey);
    sessionStorage.removeItem(this.tokenKey);
  }

}
