import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class BackendService {
  private readonly apiURL = "http://localhost:8000"

  constructor(private http: HttpClient) {
  }
}
