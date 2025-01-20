import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { Observable, throwError } from 'rxjs';
import { AuthService } from '../authorization/auth.service';
import { GroupInfoStructure, SignUpResponse, UserInfo, GroupInfo, EventInfo, CompositionInfo } from "../../interfaces"

@Injectable({
  providedIn: 'root'
})
export class BackendService {
  private readonly apiURL = "http://localhost:8000";

  constructor(private http: HttpClient, private auth: AuthService) {}

  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Authorization': `Bearer ${this.auth.getToken()}`,
    });
  }

  getUsers(group_id: number) {
    return this.http
      .get<UserInfo[]>(`${this.apiURL}/findUsers?group_id=${group_id}`, { headers: this.getHeaders() })
      .pipe(
        catchError((error) => {
          return throwError(() => error);
        })
      );
  }

  getGroups() {
    return this.http
      .get<GroupInfoStructure>(`${this.apiURL}/groups/findGroups`, { headers: this.getHeaders() })
      .pipe(
        catchError((error) => {
          return throwError(() => error);
        })
      );
  }

  getSubgroups(group_id: number) {
    return this.http
      .get<GroupInfo[]>(`${this.apiURL}/groups/findSubgroups?group_id=${group_id}`, { headers: this.getHeaders() })
      .pipe(
        catchError((error) => {
          return throwError(() => error);
        })
      );
  }

  getEvents(group_id: number) {
    return this.http
      .get<EventInfo[]>(`${this.apiURL}/events/findEvents?group_id=${group_id}`, { headers: this.getHeaders() })
      .pipe(
        catchError((error) => {
          return throwError(() => error);
        })
      );
  }

  getCatalogue(group_id: number) {
    return this.http
      .get<any>(`${this.apiURL}/catalogue/findCompositions?group_id=${group_id}`, { headers: this.getHeaders() })
      .pipe(
        catchError((error) => {
        return throwError(() => error)
        })
      )
  }

  getCatalogueExtra(group_id: number) {
    return this.http
      .get<any>(`${this.apiURL}/catalogue/findCompositionsExtra?group_id=${group_id}`, { headers: this.getHeaders() })
      .pipe(
        catchError((error) => {
        return throwError(() => error)
        })
      )
  }
  

  getAlerts(parentGroup: number) {
    return this.http
      .get<any>(`${this.apiURL}/forum/getAlerts`, {
        params: {
          parent_group: parentGroup.toString(),  // Only include parent_group as a query parameter
        },
        headers: this.getHeaders() // Assuming getHeaders() includes the Authorization header with the token
      })
      .pipe(
        catchError((error) => {
          return throwError(() => error);
        })
      );
  }
  
  
  

  postToken(token: string): Observable<SignUpResponse> {
    return this.http.post<SignUpResponse>(`${this.apiURL}/google-sign-in`, { token })
      .pipe(
        catchError((error) => {
          return throwError(() => error);
        })
      );
  }

  postRequest<T>(endpoint: string, body: any) {
    return this.http.post<T>(`${this.apiURL}/${endpoint}`, body, { headers: this.getHeaders() })
      .pipe(
        catchError((error) => {
          return throwError(() => error);
        })
      );
  }

  deleteRequest(endpoint: string, body: any) {
    return this.http.request('DELETE', `${this.apiURL}/${endpoint}`, { body: body, headers: this.getHeaders() })
      .pipe(
        catchError((error) => {
          return throwError(() => error);
        })
      );
  }
}
