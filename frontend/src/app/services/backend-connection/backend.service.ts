import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { Observable, throwError } from 'rxjs';
import { AuthService } from '../authorization/auth.service';
import { GroupInfoStructure, SignUpResponse, EventInfo } from "../../interfaces"

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

  getGroups() {
    return this.http
      .get<GroupInfoStructure>(`${this.apiURL}/groups/findGroups`, { headers: this.getHeaders() })
      .pipe(
        catchError((error) => {
        return throwError(() => error)
        })
      )
  }

  getEvents() {
    return this.http
      .get<EventInfo[]>(`${this.apiURL}/events/findEvents`, { headers: this.getHeaders() })
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

  postRequest<T>(endpoint: string, body: any) {
    return this.http.post<T>(`${this.apiURL}/${endpoint}`, body, { headers: this.getHeaders() })
      .pipe(
        catchError((error) => {
          return throwError(() => error);
        })
      )
  }
}
