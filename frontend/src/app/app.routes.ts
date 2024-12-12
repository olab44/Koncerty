import { Routes } from '@angular/router'
import { SignInComponent } from './sign-in/sign-in.component'
import { HomePageComponent } from './home-page/home-page.component'

export const routes: Routes = [
    { path: 'home', component: HomePageComponent},
    { path: '', component: SignInComponent },
    { path: '**', redirectTo: '' }
]
