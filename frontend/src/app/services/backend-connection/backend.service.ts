import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { Observable, throwError } from 'rxjs';
import { AuthService } from '../authorization/auth.service';
import { GroupInfoStructure, SignUpResponse } from "../../interfaces"

@Injectable({
  providedIn: 'root'
})
export class BackendService {
  private readonly apiURL = "http://localhost:8000"

  constructor(private http: HttpClient, private auth: AuthService) {
  }

  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Authorization': `Bearer ${this.auth.getToken()}`,
    });
  }

  mockGroupInfo() {
    return this.http
      .get<GroupInfoStructure>(`${this.apiURL}/groups/Wik`)
      .pipe(
        catchError((error) => {
        return throwError(() => error)
        })
    )
  }

  postToken(token: string): Observable<SignUpResponse> {
    return this.http.post<SignUpResponse>(`${this.apiURL}/google-sign-in`, { token })
    .pipe(
      catchError((error) => {
      return throwError(() => error)
      })
    )
  }

  postRegisterUser(username: string) {
    return this.http.post(`${this.apiURL}/createUser`, { username }, { headers: this.getHeaders() })
    .pipe(
      catchError((error) => {
      return throwError(() => error)
      })
    )
  }
}
