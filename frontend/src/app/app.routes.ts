import { Routes } from '@angular/router'

import { SignInComponent } from './sign-in/sign-in.component'
import { HomePageComponent } from './home-page/home-page.component'
import { GroupHubComponent } from './group-hub/group-hub.component'
import { MessageForumComponent } from './message-forum/message-forum.component'
import { EventCalendarComponent } from './event-calendar/event-calendar.component'
import { MusicCatalogueComponent } from './music-catalogue/music-catalogue.component'
import { EventDetailsComponent } from './event-details/event-details.component'
import { GroupControlComponent } from './group-control/group-control.component'

import { authGuard } from './services/authorization/auth.guard';

export const routes: Routes = [
    { path: 'home', component: HomePageComponent, canActivate: [authGuard] },
    { path: 'group', component: GroupHubComponent, canActivate: [authGuard] },
    { path: 'group/catalogue', component: MusicCatalogueComponent, canActivate: [authGuard] },
    { path: 'group/calendar', component: EventCalendarComponent, canActivate: [authGuard] },
    { path: 'group/event', component: EventDetailsComponent, canActivate: [authGuard] },
    { path: 'group/forum', component: MessageForumComponent, canActivate: [authGuard] },
    { path: 'group/control', component: GroupControlComponent, canActivate: [authGuard], data: { role: 'Kapelmistrz' } },
    { path: '', component: SignInComponent },
    { path: '**', redirectTo: 'home' }
]
