import { Routes } from '@angular/router'
import { SignInComponent } from './sign-in/sign-in.component'
import { HomePageComponent } from './home-page/home-page.component'
import { GroupHubComponent } from './group-hub/group-hub.component'

export const routes: Routes = [
    { path: 'home', component: HomePageComponent},
    { path: 'group/:group-name', component: GroupHubComponent},
    { path: '', component: SignInComponent },
    { path: '**', redirectTo: '' }
]
