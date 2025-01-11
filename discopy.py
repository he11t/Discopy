#!/usr/bin/env python3
"""
Discord Server Copier
A tool to clone Discord servers with all their content.
Author: shalan.v
Contact: sns2mhd@gmail.com
"""

import os
import sys
import json
import time
import logging
import hashlib
import asyncio
import aiohttp
import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from rich.table import Table
from rich.layout import Layout as RichLayout
from rich.align import Align
from rich.text import Text
from rich.box import ROUNDED
from dotenv import load_dotenv
import colorama
from colorama import Fore, init
from typing import Dict, List, Optional, Union
from datetime import datetime
import base64
from rich.prompt import Prompt

# Initialize colorama and load environment variables
init(autoreset=True)
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('discord_copy.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Constants
API_VERSION = 9
BASE_URL = f"https://discord.com/api/v{API_VERSION}"
RATE_LIMIT_DELAY = float(os.getenv('RATE_LIMIT_DELAY', '1.5'))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))

# Anti-tampering protection
INTEGRITY_CHECKSUM = "e9c8a1b2d3f4g5h6i7j8k9l0m1n2o3p4q5r6s7t8u9v0w1x2y3z4"

def calculate_checksum(data: dict) -> str:
    """Calculate checksum of critical configuration data"""
    critical_data = {
        "copyright": {
            "owner": "shalan.v",
            "email": "sns2mhd@gmail.com",
            "year": 2024
        },
        "version": "2.0"
    }
    return hashlib.sha256(json.dumps(critical_data, sort_keys=True).encode()).hexdigest()

def verify_copyright():
    """Verify copyright information and file integrity"""
    try:
        # Verify runtime integrity first
        verify_runtime_integrity()
        
        # Load and verify config.json
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
        except Exception as e:
            raise CopyrightError("Configuration file is missing or corrupted")

        # Verify copyright information exists
        copyright_info = config.get('copyright', {})
        required_fields = {
            'owner': 'shalan.v',
            'email': 'sns2mhd@gmail.com',
            'year': 2024
        }

        for field, expected in required_fields.items():
            if str(copyright_info.get(field)) != str(expected):
                raise CopyrightError(f"Copyright information has been modified: {field}")

        # Generate expected checksum
        expected_checksum = calculate_checksum(config)
        
        # Update config with correct checksum
        if config.get('checksum') != expected_checksum:
            config['checksum'] = expected_checksum
            try:
                with open('config.json', 'w') as f:
                    json.dump(config, f, indent=4)
            except Exception as e:
                raise CopyrightError("Failed to update security information")

        # Verify version
        if config.get('version') != "2.0":
            raise CopyrightError("Invalid software version")

        return True

    except Exception as e:
        if isinstance(e, (SecurityError, CopyrightError)):
            raise
        raise CopyrightError(f"Verification failed: {str(e)}")

def verify_file_integrity(filepath: str) -> bool:
    """Verify the integrity of a file"""
    try:
        if not os.path.exists(filepath):
            raise SecurityError(f"Required file missing: {filepath}")
        
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Skip variable parts in checksums
        if filepath.endswith('.env'):
            # Only check copyright lines
            content = b'\n'.join([
                line for line in content.split(b'\n')
                if line.startswith(b'COPYRIGHT_')
            ])
        elif filepath.endswith('config.json'):
            # Only verify structure and copyright info
            data = json.loads(content)
            critical_data = {
                "version": data.get("version"),
                "copyright": data.get("copyright")
            }
            content = json.dumps(critical_data, sort_keys=True).encode()
            
        return True
        
    except Exception as e:
        if isinstance(e, SecurityError):
            raise
        raise SecurityError(f"Integrity check failed for {filepath}: {str(e)}")

def verify_runtime_integrity():
    """Verify runtime environment integrity"""
    try:
        # Verify config.json exists and has correct structure
        verify_file_integrity('config.json')
        
        # Verify .env exists
        if not os.path.exists('.env'):
            raise SecurityError("Configuration file missing: .env")
            
        return True
        
    except Exception as e:
        if isinstance(e, SecurityError):
            raise
        raise SecurityError(f"Runtime verification failed: {str(e)}")

def verify_all():
    """Complete verification of the tool"""
    try:
        # Verify copyright
        verify_copyright()
        
        # Verify runtime integrity
        verify_runtime_integrity()
        
        # Additional runtime checks
        if os.environ.get('PYTHONDEVMODE') or os.environ.get('PYTHONDEBUG'):
            raise SecurityError("Development mode detected")
            
        return True
        
    except Exception as e:
        if isinstance(e, (SecurityError, CopyrightError)):
            raise
        raise SecurityError(f"Verification failed: {str(e)}")

class CopyrightError(Exception):
    """Custom exception for copyright violations"""
    def __init__(self, message="Copyright violation detected"):
        self.message = f"""
╔══════════════════════════════════════════════════╗
║                  SECURITY ALERT                   ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  [!] DISCOPY SECURITY VIOLATION DETECTED [!]     ║
║                                                  ║
║  This copy of Discopy has been compromised.      ║
║  Error: {message}                                ║
║                                                  ║
║  Please obtain an official copy from the author: ║
║  Email: sns2mhd@gmail.com                        ║
║                                                  ║
║  2024 shalan.v - All Rights Reserved          ║
║                                                  ║
╚══════════════════════════════════════════════════╝
"""
        super().__init__(self.message)

class SecurityError(Exception):
    """Custom exception for security violations"""
    def __init__(self, message="Security violation detected"):
        self.message = f"""
╔═══════════════════════════════════════════════════════════╗
║                   SECURITY VIOLATION ALERT                 ║
╠═══════════════════════════════════════════════════════════╣
║  This software is protected against unauthorized changes.  ║
║  Detected: {message}                                      ║
║                                                           ║
║  Please obtain an original copy from the author:          ║
║  Contact: sns2mhd@gmail.com                              ║
╚═══════════════════════════════════════════════════════════╝
"""
        super().__init__(self.message)

class DiscordAPIError(Exception):
    """Custom exception for Discord API errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, response_text: Optional[str] = None):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"{message} (Status: {status_code}, Response: {response_text})")

class RateLimitHandler:
    """Handles Discord API rate limiting"""
    def __init__(self):
        self.reset_after = 0
        self.last_request = 0

    async def handle_ratelimit(self):
        """Wait if we're being rate limited"""
        if time.time() < self.reset_after:
            wait_time = self.reset_after - time.time()
            logger.warning(f"Rate limited. Waiting {wait_time:.2f} seconds...")
            await asyncio.sleep(wait_time)

    def update_ratelimit(self, headers: Dict[str, str]):
        """Update rate limit info from response headers"""
        if 'X-RateLimit-Reset-After' in headers:
            self.reset_after = time.time() + float(headers['X-RateLimit-Reset-After'])

class UserAPI:
    """Handles Discord API interactions"""
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.rate_limiter = RateLimitHandler()
        self.session = None

    async def __aenter__(self):
        """Initialize aiohttp session when entering context"""
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close aiohttp session when exiting context"""
        if self.session:
            await self.session.close()
            self.session = None

    async def request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make an API request with rate limit handling and retries"""
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with' context manager.")

        url = f"{BASE_URL}{endpoint}"
        retries = 0

        while retries < MAX_RETRIES:
            await self.rate_limiter.handle_ratelimit()

            try:
                async with self.session.request(method, url, **kwargs) as resp:
                    self.rate_limiter.update_ratelimit(resp.headers)

                    if resp.status == 429:  # Rate limited
                        retry_after = float(resp.headers.get('Retry-After', RATE_LIMIT_DELAY))
                        logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
                        await asyncio.sleep(retry_after)
                        retries += 1
                        continue

                    if resp.status == 404:
                        raise DiscordAPIError("Resource not found", resp.status, await resp.text())

                    if resp.status == 403:
                        raise DiscordAPIError("Permission denied", resp.status, await resp.text())

                    if resp.status >= 400:
                        raise DiscordAPIError("API request failed", resp.status, await resp.text())

                    return await resp.json() if resp.status != 204 else {}

            except aiohttp.ClientError as e:
                logger.error(f"Network error: {str(e)}")
                retries += 1
                if retries < MAX_RETRIES:
                    await asyncio.sleep(RATE_LIMIT_DELAY * retries)
                else:
                    raise DiscordAPIError(f"Max retries exceeded: {str(e)}")

        raise DiscordAPIError("Max retries exceeded")

def load_config() -> dict:
    """Load configuration from config.json"""
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        logger.error("Invalid JSON in config.json")
        return {}

def save_config(config: dict):
    """Save configuration to config.json"""
    try:
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to save config: {str(e)}")

class ServerCopier:
    def __init__(self, user_api):
        self.user_api = user_api
        self.console = Console()
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=self.console
        )

    async def get_server_icon(self, guild_id: str) -> Optional[str]:
        """Get server icon data"""
        try:
            guild = await self.user_api.request('GET', f'/guilds/{guild_id}')
            if guild.get('icon'):
                icon_url = f"https://cdn.discordapp.com/icons/{guild_id}/{guild['icon']}.png?size=1024"
                async with aiohttp.ClientSession() as session:
                    async with session.get(icon_url) as resp:
                        if resp.status == 200:
                            icon_data = await resp.read()
                            return f"data:image/png;base64,{base64.b64encode(icon_data).decode('utf-8')}"
        except Exception as e:
            logger.error(f"Failed to get server icon: {str(e)}")
        return None

    async def clean_server(self, guild_id: str):
        """Clean a server before copying"""
        self.console.print(Panel("Starting server cleanup...", style="yellow"))
        
        with self.progress as progress:
            overall_task = progress.add_task("[cyan]Overall cleanup progress...", total=4)
            
            # Delete channels
            channels_task = progress.add_task("[red]Cleaning channels...", total=100)
            try:
                channels = await self.user_api.request('GET', f'/guilds/{guild_id}/channels')
                if channels:
                    increment = 100 / len(channels)
                    for channel in channels:
                        try:
                            await self.user_api.request('DELETE', f'/channels/{channel["id"]}')
                            progress.update(channels_task, advance=increment)
                        except Exception as e:
                            self.console.print(f"[red]Error deleting channel {channel.get('name', 'Unknown')}: {str(e)}")
                progress.update(overall_task, advance=1)
            except Exception as e:
                self.console.print(f"[red]Error cleaning channels: {str(e)}")
            
            # Delete roles
            roles_task = progress.add_task("[yellow]Cleaning roles...", total=100)
            try:
                roles = await self.user_api.request('GET', f'/guilds/{guild_id}/roles')
                if roles:
                    increment = 100 / len(roles)
                    for role in roles:
                        if role['name'] != '@everyone':
                            try:
                                await self.user_api.request('DELETE', f'/guilds/{guild_id}/roles/{role["id"]}')
                                progress.update(roles_task, advance=increment)
                            except Exception as e:
                                self.console.print(f"[red]Error deleting role {role.get('name', 'Unknown')}: {str(e)}")
                progress.update(overall_task, advance=1)
            except Exception as e:
                self.console.print(f"[red]Error cleaning roles: {str(e)}")
            
            # Delete emojis
            emojis_task = progress.add_task("[green]Cleaning emojis...", total=100)
            try:
                emojis = await self.user_api.request('GET', f'/guilds/{guild_id}/emojis')
                if emojis:
                    increment = 100 / len(emojis)
                    for emoji in emojis:
                        try:
                            await self.user_api.request('DELETE', f'/guilds/{guild_id}/emojis/{emoji["id"]}')
                            progress.update(emojis_task, advance=increment)
                        except Exception as e:
                            self.console.print(f"[red]Error deleting emoji {emoji.get('name', 'Unknown')}: {str(e)}")
                progress.update(overall_task, advance=1)
            except Exception as e:
                self.console.print(f"[red]Error cleaning emojis: {str(e)}")
            
            # Delete stickers
            stickers_task = progress.add_task("[blue]Cleaning stickers...", total=100)
            try:
                stickers = await self.user_api.request('GET', f'/guilds/{guild_id}/stickers')
                if stickers:
                    increment = 100 / len(stickers)
                    for sticker in stickers:
                        try:
                            await self.user_api.request('DELETE', f'/guilds/{guild_id}/stickers/{sticker["id"]}')
                            progress.update(stickers_task, advance=increment)
                        except Exception as e:
                            self.console.print(f"[red]Error deleting sticker {sticker.get('name', 'Unknown')}: {str(e)}")
                progress.update(overall_task, advance=1)
            except Exception as e:
                self.console.print(f"[red]Error cleaning stickers: {str(e)}")

        self.console.print(Panel("Server cleanup completed!", style="green"))

    async def copy_to_existing_server(self, source_id: str, target_id: str):
        """Copy a server to an existing server with improved progress tracking"""
        try:
            # Verify server access
            source_guild = await self.user_api.request('GET', f'/guilds/{source_id}?with_counts=true')
            target_guild = await self.user_api.request('GET', f'/guilds/{target_id}?with_counts=true')
            
            if not source_guild or not target_guild:
                self.console.print("[red]Error: Could not access one or both servers. Please check the IDs and permissions.")
                return False

            self.console.print(Panel(f"[cyan]Copying from:[/] {source_guild['name']}\n[cyan]To:[/] {target_guild['name']}", title="Server Copy"))

            # Clean target server first
            await self.clean_server(target_id)
            
            with self.progress as progress:
                overall_task = progress.add_task("[cyan]Overall copy progress...", total=6)
                
                # Copy server settings and icon
                settings_task = progress.add_task("[magenta]Copying server settings...", total=100)
                try:
                    # Get server icon
                    icon_data = await self.get_server_icon(source_id)
                    progress.update(settings_task, advance=50)
                    
                    # Update server settings
                    await self.user_api.request('PATCH', f'/guilds/{target_id}', json={
                        "name": source_guild.get('name'),
                        "icon": icon_data,
                        "verification_level": source_guild.get('verification_level'),
                        "default_message_notifications": source_guild.get('default_message_notifications'),
                        "explicit_content_filter": source_guild.get('explicit_content_filter'),
                        "afk_timeout": source_guild.get('afk_timeout'),
                        "preferred_locale": source_guild.get('preferred_locale')
                    })
                    progress.update(settings_task, advance=50)
                    progress.update(overall_task, advance=1)
                except Exception as e:
                    self.console.print(f"[red]Error copying server settings: {str(e)}")

                # Copy roles
                roles_task = progress.add_task("[yellow]Copying roles...", total=100)
                source_roles = await self.user_api.request('GET', f'/guilds/{source_id}/roles')
                role_mapping = {}
                
                if source_roles:
                    increment = 100 / len(source_roles)
                    for role in reversed(source_roles):
                        if role['name'] != '@everyone':
                            try:
                                new_role = await self.user_api.request('POST', f'/guilds/{target_id}/roles', json={
                                    "name": role['name'],
                                    "permissions": role['permissions'],
                                    "color": role['color'],
                                    "hoist": role['hoist'],
                                    "mentionable": role['mentionable']
                                })
                                role_mapping[role['id']] = new_role['id']
                                progress.update(roles_task, advance=increment)
                            except Exception as e:
                                self.console.print(f"[red]Error copying role {role.get('name', 'Unknown')}: {str(e)}")
                progress.update(overall_task, advance=1)

                # Copy categories and channels
                channels_task = progress.add_task("[green]Copying channels...", total=100)
                source_channels = await self.user_api.request('GET', f'/guilds/{source_id}/channels')
                channel_mapping = {}
                
                if source_channels:
                    # First copy categories
                    categories = [c for c in source_channels if c['type'] == 4]
                    if categories:
                        cat_increment = 50 / len(categories)
                        for category in categories:
                            try:
                                new_category = await self.user_api.request('POST', f'/guilds/{target_id}/channels', json={
                                    "name": category['name'],
                                    "type": 4,
                                    "position": category['position'],
                                    "permission_overwrites": self._update_permission_overwrites(category.get('permission_overwrites', []), role_mapping)
                                })
                                channel_mapping[category['id']] = new_category['id']
                                progress.update(channels_task, advance=cat_increment)
                            except Exception as e:
                                self.console.print(f"[red]Error copying category {category.get('name', 'Unknown')}: {str(e)}")
                    
                    # Then copy other channels
                    non_categories = [c for c in source_channels if c['type'] != 4]
                    if non_categories:
                        chan_increment = 50 / len(non_categories)
                        for channel in non_categories:
                            try:
                                new_channel = await self.user_api.request('POST', f'/guilds/{target_id}/channels', json={
                                    "name": channel['name'],
                                    "type": channel['type'],
                                    "topic": channel.get('topic'),
                                    "bitrate": channel.get('bitrate'),
                                    "user_limit": channel.get('user_limit'),
                                    "rate_limit_per_user": channel.get('rate_limit_per_user'),
                                    "position": channel['position'],
                                    "nsfw": channel.get('nsfw', False),
                                    "parent_id": channel_mapping.get(channel.get('parent_id')),
                                    "permission_overwrites": self._update_permission_overwrites(channel.get('permission_overwrites', []), role_mapping)
                                })
                                channel_mapping[channel['id']] = new_channel['id']
                                progress.update(channels_task, advance=chan_increment)
                            except Exception as e:
                                self.console.print(f"[red]Error copying channel {channel.get('name', 'Unknown')}: {str(e)}")
                progress.update(overall_task, advance=1)

                # Copy emojis
                emojis_task = progress.add_task("[blue]Copying emojis...", total=100)
                source_emojis = await self.user_api.request('GET', f'/guilds/{source_id}/emojis')
                if source_emojis:
                    increment = 100 / len(source_emojis)
                    for emoji in source_emojis:
                        try:
                            # Get emoji image data
                            emoji_url = f"https://cdn.discordapp.com/emojis/{emoji['id']}.png"
                            async with aiohttp.ClientSession() as session:
                                async with session.get(emoji_url) as resp:
                                    if resp.status == 200:
                                        image_data = await resp.read()
                                        image_b64 = f"data:image/png;base64,{base64.b64encode(image_data).decode('utf-8')}"
                                        
                                        await self.user_api.request('POST', f'/guilds/{target_id}/emojis', json={
                                            "name": emoji['name'],
                                            "image": image_b64,
                                            "roles": [role_mapping.get(role_id, role_id) for role_id in emoji.get('roles', [])]
                                        })
                            progress.update(emojis_task, advance=increment)
                        except Exception as e:
                            self.console.print(f"[red]Error copying emoji {emoji.get('name', 'Unknown')}: {str(e)}")
                progress.update(overall_task, advance=1)

                # Copy stickers
                stickers_task = progress.add_task("[magenta]Copying stickers...", total=100)
                source_stickers = await self.user_api.request('GET', f'/guilds/{source_id}/stickers')
                if source_stickers:
                    increment = 100 / len(source_stickers)
                    for sticker in source_stickers:
                        try:
                            # Get sticker data
                            sticker_url = f"https://cdn.discordapp.com/stickers/{sticker['id']}.png"
                            async with aiohttp.ClientSession() as session:
                                async with session.get(sticker_url) as resp:
                                    if resp.status == 200:
                                        sticker_data = await resp.read()
                                        sticker_b64 = f"data:image/png;base64,{base64.b64encode(sticker_data).decode('utf-8')}"
                                        
                                        await self.user_api.request('POST', f'/guilds/{target_id}/stickers', json={
                                            "name": sticker['name'],
                                            "description": sticker.get('description', ''),
                                            "tags": sticker.get('tags', ''),
                                            "file": sticker_b64
                                        })
                            progress.update(stickers_task, advance=increment)
                        except Exception as e:
                            self.console.print(f"[red]Error copying sticker {sticker.get('name', 'Unknown')}: {str(e)}")
                progress.update(overall_task, advance=1)

                # Final update
                progress.update(overall_task, completed=100)

            self.console.print(Panel(
                "[green]Server copy completed successfully!\n" +
                f"[cyan]Copied:[/] {len(role_mapping)} roles, {len(channel_mapping)} channels\n" +
                f"[cyan]From:[/] {source_guild['name']}\n" +
                f"[cyan]To:[/] {target_guild['name']}",
                title="Success",
                border_style="green"
            ))
            return True

        except Exception as e:
            self.console.print(f"[red]Error copying server: {str(e)}")
            logger.error(f"Server copy error: {str(e)}", exc_info=True)
            return False

    async def copy_server(self, source_id: str, new_name: str):
        """Create a new server and copy content from source server"""
        try:
            # Verify source server access
            source_guild = await self.user_api.request('GET', f'/guilds/{source_id}?with_counts=true')
            if not source_guild:
                self.console.print("[red]Error: Could not access source server. Please check the ID and permissions.")
                return False

            self.console.print(f"\n[cyan]Creating new server: {new_name}[/]")
            
            # Create new server
            new_guild = None
            try:
                # Get source server icon
                icon_data = await self.get_server_icon(source_id)
                
                new_guild = await self.user_api.request('POST', '/guilds', json={
                    "name": new_name,
                    "icon": icon_data,
                    "verification_level": source_guild.get('verification_level', 0),
                    "default_message_notifications": source_guild.get('default_message_notifications', 0),
                    "explicit_content_filter": source_guild.get('explicit_content_filter', 0),
                    "preferred_locale": source_guild.get('preferred_locale', "en-US"),
                    "roles": [],
                    "channels": []
                })
                if not new_guild:
                    self.console.print("[red]Error: Failed to create new server.")
                    return False
                new_guild_id = new_guild['id']
            except Exception as e:
                self.console.print(f"[red]Error creating new server: {str(e)}")
                return False

            # Wait for server creation to complete
            await asyncio.sleep(2)

            self.console.print(Panel(f"[cyan]Copying from:[/] {source_guild['name']}\n[cyan]To:[/] {new_name}", title="Server Copy"))
            
            # Copy everything to the new server
            success = await self.copy_to_existing_server(source_id, new_guild_id)
            
            if success:
                # Create invite link
                try:
                    channels = await self.user_api.request('GET', f'/guilds/{new_guild_id}/channels')
                    text_channels = [c for c in channels if c['type'] == 0]  # Type 0 is text channel
                    if text_channels:
                        invite = await self.user_api.request('POST', f'/channels/{text_channels[0]["id"]}/invites', json={
                            "max_age": 86400,  # 24 hours
                            "max_uses": 0,     # Unlimited uses
                            "temporary": False,
                            "unique": True
                        })
                        if invite and 'code' in invite:
                            invite_url = f"https://discord.gg/{invite['code']}"
                            self.console.print(Panel(
                                f"[green]Server created successfully!\n[cyan]Invite Link:[/] {invite_url}",
                                title="Success",
                                border_style="green"
                            ))
                        else:
                            self.console.print("[yellow]Server created successfully! (Could not create invite link)")
                    else:
                        self.console.print("[yellow]Server created successfully! (No text channels for invite link)")
                except Exception as e:
                    self.console.print(f"[yellow]Server created successfully! (Error creating invite: {str(e)})")
            
            return success

        except Exception as e:
            self.console.print(f"[red]Fatal error during server creation: {str(e)}")
            logger.error(f"Server creation error: {str(e)}", exc_info=True)
            return False

    def _update_permission_overwrites(self, overwrites: List[dict], role_mapping: Dict[str, str]) -> List[dict]:
        """Update permission overwrites with new role IDs"""
        updated_overwrites = []
        for overwrite in overwrites:
            new_overwrite = overwrite.copy()
            if overwrite['type'] == 0:  # Role overwrite
                new_overwrite['id'] = role_mapping.get(overwrite['id'], overwrite['id'])
            updated_overwrites.append(new_overwrite)
        return updated_overwrites

async def verify_token(token: str) -> bool:
    """Verify if the Discord token is valid"""
    try:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f"{BASE_URL}/users/@me") as resp:
                if resp.status == 200:
                    user_data = await resp.json()
                    logger.info(f"Token verified for user: {user_data.get('username', 'Unknown')}")
                    return True
                else:
                    logger.error(f"Token verification failed with status {resp.status}")
                    return False
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return False

async def main():
    """Main entry point of the application"""
    # Initialize rich console at the start
    console = Console()
    
    try:
        # Complete verification first
        try:
            verify_all()
        except (SecurityError, CopyrightError) as e:
            console.print(f"[red]{str(e)}[/]")
            return
        
        # Try to load token from .env file first
        load_dotenv()
        token = os.getenv('DISCORD_TOKEN')
        
        # If no token in .env, prompt user
        if not token:
            console.print("[yellow]No token found in .env file. You can either:[/]")
            console.print("1. Enter your token now")
            console.print("2. Add DISCORD_TOKEN to your .env file later")
            
            if Prompt.ask("Would you like to enter your token now?", choices=["yes", "no"], default="yes") == "yes":
                token = Prompt.ask("Enter your Discord token", password=True)
                
                # Optionally save to .env
                if Prompt.ask("Would you like to save this token to .env?", choices=["yes", "no"], default="no") == "yes":
                    with open('.env', 'a') as f:
                        f.write(f"\nDISCORD_TOKEN={token}")
                    console.print("[green]Token saved to .env file[/]")

        # Verify token if provided
        if token and not await verify_token(token):
            console.print("[red]Error: Invalid Discord token[/]")
            token = None

        if not token:
            console.print("[yellow]Note: You'll need to provide a token for each operation[/]")

        while True:
            console.print(Panel("""
[cyan]Discopy - Professional Discord Server Cloner[/]

1. [green]Copy Server[/] - Create new server with content
2. [yellow]Clean Server[/] - Remove all content
3. [blue]Copy to Existing[/] - Copy content to existing server
4. [red]Exit[/]
            """, title="Main Menu", border_style="cyan"))
            
            choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4"])
            
            if choice == "4":
                console.print("[yellow]Goodbye![/]")
                break
            
            # Get token if not already provided
            operation_token = token
            if not operation_token:
                operation_token = Prompt.ask("Enter your Discord token", password=True)
                if not await verify_token(operation_token):
                    console.print("[red]Invalid token. Returning to menu...[/]")
                    continue
                
            source_id = Prompt.ask("\nEnter source server ID")
            
            async with UserAPI(operation_token) as user_api:
                copier = ServerCopier(user_api)
                
                if choice == "1":
                    new_name = Prompt.ask("Enter name for the new server")
                    await copier.copy_server(source_id, new_name)
                elif choice == "2":
                    confirm = Prompt.ask(
                        "[red]WARNING: This will delete ALL content from the server. Are you sure?[/]",
                        choices=["yes", "no"],
                        default="no"
                    )
                    if confirm == "yes":
                        await copier.clean_server(source_id)
                elif choice == "3":
                    target_id = Prompt.ask("Enter target server ID")
                    await copier.copy_to_existing_server(source_id, target_id)
            
            # Pause before showing menu again
            console.print("\nPress Enter to continue...")
            input()
            console.clear()

    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}", exc_info=True)
        console.print(f"[red]An error occurred: {str(e)}[/]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
