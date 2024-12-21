import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';

import { GroupInfoStructure } from "../../interfaces"

@Injectable({
  providedIn: 'root'
})
export class BackendService {
  private readonly apiURL = "http://localhost:8000"

  constructor(private http: HttpClient) {
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

  postToken(token: string) {
    return this.http
    .post(`${this.apiURL}/google-sign-in`, { token })
    .pipe(
      catchError((error) => {
      return throwError(() => error)
      })
    )
  }
}
