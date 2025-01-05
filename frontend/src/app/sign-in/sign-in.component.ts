import { Component, OnInit, NgZone } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TranslateModule } from "@ngx-translate/core";
import { Router } from '@angular/router';
import { TopBarComponent } from '../bars/top-bar/top-bar.component';
import { AuthService } from '../services/authorization/auth.service';
import { BackendService } from '../services/backend-connection/backend.service';
import { SignUpResponse } from '../interfaces';

declare var google: any;

@Component({
  selector: 'app-sign-in',
  standalone: true,
  imports: [ CommonModule, FormsModule, TranslateModule, TopBarComponent ],
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.css'
})
export class SignInComponent implements OnInit {
  constructor(
    private backend: BackendService,
    private router: Router,
    public auth: AuthService,
    private ngZone: NgZone,
  ) {}

  promptUsername: boolean = false
  username: string = '';

  ngOnInit(): void {
    // Initialize the Google Sign-In Client
    google.accounts.id.initialize({
      client_id:"67926087995-g4ub7nr9u0mqooermb5hvhd1794pvvfq.apps.googleusercontent.com",
      context: "signin",
      ux_mode: "popup",
      callback: (response: any) => this.handleCredentialsResponse(response),
    })

    google.accounts.id.renderButton(
      document.getElementById('sign-in-icon'),
      { type: 'icon', size: 'large', theme: 'filled_black' }
    )
  }

  handleCredentialsResponse(response: any): void {
    this.backend.postToken(response.credential).subscribe({
      next: (response: SignUpResponse) => {
        const token = response.app_token
        this.auth.setToken(token)
        this.ngZone.run(() => this.promptUsername = response.new);

        if (!response.new) {
          this.auth.setLoggedIn(true)
          this.ngZone.run(() => { this.router.navigate(['/home']) })
        }
      },
      error: (error) => {
        console.error('Error during signIn:', error);
      },
    });
  }

  setUsername(username: string) {
    this.backend.postRequest('createUser', {username}).subscribe({
      next: (response) => {
        this.auth.setLoggedIn(true)
        this.ngZone.run(() => { this.promptUsername = false; this.router.navigate(['/home']) })
      },
      error: (error) => {
        console.error('Error during signUp:', error);
      },
    });
  }
}
