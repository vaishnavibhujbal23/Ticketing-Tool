from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Ticket, User
from django.views.decorators.http import require_POST
from .forms import TicketForm, CommentForm, CustomUserCreationForm
from django.contrib.auth import login,logout

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('ticket_list')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def ticket_list(request):
    status_filter = request.GET.get('status', '')
    
    if request.user.is_superuser:
        return redirect('manage_tickets')
    
    # Filter tickets based on user role
    if request.user.is_engineer():
        # Engineers see tickets assigned to them
        tickets = Ticket.objects.filter(assigned_engineer=request.user)
    else:
        # Regular users see tickets they created
        tickets = Ticket.objects.filter(creator=request.user)
    
    if status_filter and status_filter != 'ALL':
        tickets = tickets.filter(status=status_filter)
    
    return render(request, 'tickets/ticket_list.html', {
        'tickets': tickets,
        'user_type': request.user.user_type,
        'status_choices': dict(Ticket.STATUS_CHOICES),
        'current_status': status_filter
        })

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    # Check if user has permission to view this ticket
    if not (request.user == ticket.creator or 
            request.user == ticket.assigned_engineer or 
            request.user.is_superuser):
        raise PermissionDenied
    
    comments = ticket.comments.all().order_by('-created_at')
    status_choices = Ticket.STATUS_CHOICES

    if request.method == 'POST':
        if not ticket.can_comment(request.user):
            raise PermissionDenied
            
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('ticket_detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'comment_form': comment_form,
        'status_choices': status_choices,
        'can_update_status': ticket.can_update_status(request.user),
        'can_comment': ticket.can_comment(request.user)
    })

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.creator = request.user
            ticket.save()
            messages.success(request, 'Ticket created successfully.')
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm()
    return render(request, 'tickets/create_ticket.html', {'form': form})

@login_required
@require_POST
def update_ticket_status(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if not ticket.can_update_status(request.user):
        raise PermissionDenied
        
    new_status = request.POST.get('status')
    if new_status in dict(Ticket.STATUS_CHOICES):
        ticket.status = new_status
        ticket.save()
        messages.success(request, 'Ticket status updated successfully.')
    return redirect('ticket_detail', pk=pk)

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def manage_tickets(request):
    """View for superusers to manage all tickets"""
    status_filter = request.GET.get('status', '')
    assignment_filter = request.GET.get('assignment', '')
    
    tickets = Ticket.objects.all().select_related('creator', 'assigned_engineer')
    
    if status_filter and status_filter != 'ALL':
        tickets = tickets.filter(status=status_filter)
        
    if assignment_filter:
        if assignment_filter == 'unassigned':
            tickets = tickets.filter(assigned_engineer=None)
        elif assignment_filter == 'assigned':
            tickets = tickets.filter(assigned_engineer__isnull=False)
    
    engineers = User.objects.filter(user_type='ENGINEER')
    
    return render(request, 'tickets/manage_tickets.html', {
        'tickets': tickets,
        'engineers': engineers,
        'status_choices': dict(Ticket.STATUS_CHOICES),
        'current_status': status_filter,
        'current_assignment': assignment_filter
    })

@login_required
@user_passes_test(is_superuser)
def assign_engineer(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    if request.method == 'POST':
        engineer_id = request.POST.get('assigned_engineer')
        try:
            engineer = User.objects.get(id=engineer_id, user_type='ENGINEER')
            ticket.assigned_engineer = engineer
            ticket.save()
            messages.success(
                request, 
                f'Ticket successfully assigned to {engineer.get_full_name() or engineer.username}'
            )
        except User.DoesNotExist:
            messages.error(request, 'Invalid engineer selected.')
    
    return redirect(request.POST.get('next', 'manage_tickets'))